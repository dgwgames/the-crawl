# tests/test_world_generation_service.py

import pytest
import logging

import json

from app.core.services.world_generation_service import WorldGenerationService
from app.db.models import RoomModel
from tests.fixtures import setup_test_db

logger = logging.getLogger(__name__)


@pytest.fixture
def world_service(setup_test_db):
    """
    Fixture to set up the WorldGenerationService with a test database connection.
    """
    return WorldGenerationService(setup_test_db)


@pytest.mark.asyncio
async def test_generate_map_room(world_service):
    """
    Test generating a map room using GPT response.
    """
    logger.info("Starting test: test_generate_map_room")

    # Given
    prompt = """
    Generate a map location for a grid-based text game. The map room is an outdoor location. 
    The response should be a JSON object with the following structure:

    {
      "name": "Room Name",
      "description": "A detailed description of the room.",
      "coordinates": {"x": 0, "y": 0},
      "features": [
        {"type": "feature type", "description": "A description of the feature"}
      ],
      "sounds": ["list of sounds"],
      "smells": ["list of smells"]
    }
    Ensure the response is strictly in this format.
    """

    # When
    result = await world_service.generate_map_room(prompt)
    logger.info(f"Generated room: {result}")

    # Then
    assert "name" in result, f"Expected 'name' in result, got: {result}"
    assert "description" in result, f"Expected 'description' in result, got: {result}"
    assert "grid_coordinates" in result, f"Expected 'grid_coordinates' in result, got: {result}"
    assert isinstance(result["grid_coordinates"],
                      dict), f"Expected 'grid_coordinates' to be a dict, got: {type(result['grid_coordinates'])}"
    assert "x" in result["grid_coordinates"] and "y" in result[
        "grid_coordinates"], "Expected 'x' and 'y' in grid_coordinates"


@pytest.mark.asyncio
async def test_generate_connected_room(world_service):
    """
    Test generating a connected map room or handling location-occupied errors.
    """
    logger.info("Starting test: test_generate_connected_room")

    # Given
    current_coordinates = {"x": 0, "y": 0}
    direction = "east"

    # When
    result = await world_service.generate_connected_room(current_coordinates=current_coordinates, direction=direction)
    logger.info(f"Generated connected room: {json.dumps(result, indent=4)}")

    # Check if the result contains an error about the location being occupied
    if "error" in result and result["error"] == "Location occupied":
        # Handle the location occupied case
        assert result["error"] == "Location occupied", f"Expected 'Location occupied' error, got: {result['error']}"
    else:
        # Check that we have new locations
        assert "new_locations" in result, f"Expected 'new_locations' in result, got: {result}"

        # Iterate through new locations and run assertions
        for location in result["new_locations"]:
            assert "name" in location, f"Expected 'name' in location, got: {location}"
            assert "description" in location, f"Expected 'description' in location, got: {location}"
            assert "coords" in location, f"Expected 'coords' in location, got: {location}"

            # Check coordinate types
            assert isinstance(location["coords"], dict), \
                f"Expected 'coords' to be a dict, got: {type(location['coords'])}"
            assert "x" in location["coords"], f"Expected 'x' in coords"
            assert "y" in location["coords"], f"Expected 'y' in coords"

            # Assertions for features, sounds, and smells
            assert "features" in location, f"Expected 'features' in location, got: {location}"
            assert isinstance(location["features"], list), \
                f"Expected 'features' to be a list, got: {type(location['features'])}"

            assert "sounds" in location, f"Expected 'sounds' in location, got: {location}"
            assert isinstance(location["sounds"], list), \
                f"Expected 'sounds' to be a list, got: {type(location['sounds'])}"

            assert "smells" in location, f"Expected 'smells' in location, got: {location}"
            assert isinstance(location["smells"], list), \
                f"Expected 'smells' to be a list, got: {type(location['smells'])}"


def test_get_room_by_coordinates(setup_test_db):
    logger.info("Starting test: test_get_room_by_coordinates")
    """Test retrieving a room by its coordinates."""
    # Given
    room_name = "HiddenChamber"
    room_description = "A secret room hidden behind a false wall."
    x_coordinate = 3
    y_coordinate = 4
    RoomModel.create_room(setup_test_db, name=room_name, description=room_description, x_coordinate=x_coordinate, y_coordinate=y_coordinate)

    logger.info(f"Retrieving room by coordinates: ({x_coordinate}, {y_coordinate})")
    # When
    room = RoomModel.get_room_by_coordinates(setup_test_db, coordinates={"x": x_coordinate, "y": y_coordinate})

    # Then
    assert room is not None, "Expected to retrieve a room, got None"
    assert room["name"] == room_name, f"Expected room name to be {room_name}, got {room['name']}"

def test_get_room_by_name(setup_test_db):
    logger.info("Starting test: test_get_room_by_name")
    """Test retrieving a room by its name."""
    # Given
    room_name = "HiddenChamber"
    room_description = "A secret room hidden behind a false wall."
    x_coordinate = 3
    y_coordinate = 4
    RoomModel.create_room(setup_test_db, name=room_name, description=room_description, x_coordinate=x_coordinate, y_coordinate=y_coordinate)

    logger.info("Retrieving room by name: %s", room_name)
    # When
    room = RoomModel.get_room_by_name(setup_test_db, name=room_name)

    # Then
    logger.info("Asserting the room has been retrieved correctly.")
    assert room is not None
    assert room["name"] == room_name
    assert room["description"] == room_description
    assert room["x_coordinate"] == x_coordinate
    assert room["y_coordinate"] == y_coordinate