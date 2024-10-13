# tests/test_world_generation_service.py

import pytest
import logging
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
    prompt = "The map room is an outdoor location."

    # When
    result = await world_service.generate_map_room(prompt)

    # Then
    assert "name" in result, f"Expected 'name' in result, got: {result}"
    assert "description" in result, f"Expected 'description' in result, got: {result}"
    assert "grid_coordinates" in result, f"Expected 'grid_coordinates' in result, got: {result}"
    assert isinstance(result["grid_coordinates"],
                      dict), f"Expected 'grid_coordinates' to be a dict, got: {type(result['grid_coordinates'])}"
    assert "x" in result["grid_coordinates"] and "y" in result[
        "grid_coordinates"], "Expected 'x' and 'y' in grid_coordinates"
    logger.info(f"Generated room: {result}")


@pytest.mark.asyncio
async def test_generate_connected_room(world_service):
    """
    Test generating a connected map room.
    """
    logger.info("Starting test: test_generate_connected_room")
    # Given
    current_coordinates = {"x": 5, "y": 5}
    direction = "east"

    # When
    result = await world_service.generate_connected_room(current_coordinates=current_coordinates, direction=direction)

    # Then
    assert "name" in result, f"Expected 'name' in result, got: {result}"
    assert "description" in result, f"Expected 'description' in result, got: {result}"
    assert "grid_coordinates" in result, f"Expected 'grid_coordinates' in result, got: {result}"
    assert isinstance(result["grid_coordinates"],
                      dict), f"Expected 'grid_coordinates' to be a dict, got: {type(result['grid_coordinates'])}"
    assert "x" in result["grid_coordinates"] and "y" in result[
        "grid_coordinates"], "Expected 'x' and 'y' in grid_coordinates"
    assert result["grid_coordinates"] != current_coordinates, "Coordinates should be updated for the connected room"
    logger.info(f"Generated connected room: {result}")

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