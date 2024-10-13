import logging
from app.db.models import PlayerModel, RoomModel
from tests.fixtures import setup_test_db

logger = logging.getLogger(__name__)


def test_create_player(setup_test_db):
    logger.info("Starting test: test_create_player")
    """Test inserting a new player into the database."""
    # Given
    player_name = "TestPlayer"

    logger.info("Creating player with name: %s", player_name)
    # When
    PlayerModel.create_player(setup_test_db, name=player_name)

    # Then
    logger.info("Asserting the player has been inserted into the database.")
    player = setup_test_db.execute("SELECT * FROM players WHERE name = ?", (player_name,)).fetchone()
    assert player is not None
    assert player["name"] == player_name
    assert player["current_room"] == "start"


def test_update_player_location(setup_test_db):
    logger.info("Starting test: test_update_player_location")
    """Test updating a player's current room."""
    # Given
    player_name = "TestPlayer"
    PlayerModel.create_player(setup_test_db, name=player_name)
    player = setup_test_db.execute("SELECT * FROM players WHERE name = ?", (player_name,)).fetchone()
    player_dict = dict(player)  # Convert Row object to dictionary

    logger.info("Updating player location to 'east_room'.")
    # When
    PlayerModel.update_player_location(setup_test_db, player_name=player_dict["name"], new_room="east_room")

    # Then
    logger.info("Asserting the player's location has been updated.")
    updated_player = setup_test_db.execute("SELECT * FROM players WHERE name = ?", (player_dict["name"],)).fetchone()
    player_dict = dict(updated_player)  # Convert Row object to dictionary
    assert player_dict["current_room"] == "east_room"


def test_create_room(setup_test_db):
    logger.info("Starting test: test_create_room")
    """Test inserting a new room into the database."""
    # Given
    room_name = "TreasureRoom"
    room_description = "A room filled with treasure."
    x_coordinate = 1
    y_coordinate = 2

    logger.info("Creating room with name: %s, description: %s, coordinates: (%d, %d)", room_name, room_description, x_coordinate, y_coordinate)
    # When
    RoomModel.create_room(setup_test_db, name=room_name, description=room_description, x_coordinate=x_coordinate, y_coordinate=y_coordinate)

    # Then
    logger.info("Asserting the room has been inserted into the database.")
    room = setup_test_db.execute("SELECT * FROM rooms WHERE name = ?", (room_name,)).fetchone()
    assert room is not None
    assert room["name"] == room_name
    assert room["description"] == room_description
    assert room["x_coordinate"] == x_coordinate
    assert room["y_coordinate"] == y_coordinate


