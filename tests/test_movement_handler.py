import pytest
from app.db.models import PlayerModel, RoomModel
from app.core.movement_handler import MovementHandler
from app.db.database import get_singleton_db_connection, init_db


# Test fixtures help set up and tear down a shared persistent database for testing
@pytest.fixture(scope="function")
def setup_test_db():
    """Sets up a persistent SQLite database for testing using the singleton connection."""
    # Get the singleton SQLite database connection
    connection = get_singleton_db_connection()

    # Initialize tables if they do not exist
    init_db()
    PlayerModel.create_table(connection)
    RoomModel.create_table(connection)

    # Clear any existing data to ensure a clean state
    connection.execute("DELETE FROM players;")
    connection.execute("DELETE FROM rooms;")

    # Create initial rooms
    RoomModel.create_room(connection, "start", "The starting point of your journey.")
    RoomModel.create_room(connection, "east_room", "You have entered the east room.")
    RoomModel.create_room(connection, "west_room", "You have entered the west room.")

    yield connection  # Provide the connection to the test function

    # Teardown: Clear data after each test to maintain isolation
    connection.execute("DELETE FROM players;")
    connection.execute("DELETE FROM rooms;")


def test_movement_handler_move_valid(setup_test_db):
    """Test that a player can successfully move between rooms using MovementHandler."""
    # Given
    player_name = "TestPlayer"
    PlayerModel.create_player(setup_test_db, name=player_name)
    movement_handler = MovementHandler()

    # When - Player moves east
    result = movement_handler.move_player(setup_test_db, player_name, "east")

    # Then
    assert result["success"] is True
    assert result["message"] == "You have moved to the east_room."
    player = PlayerModel.get_player_by_name(setup_test_db, player_name)
    player_dict = dict(player)  # Convert Row object to dictionary
    assert player_dict["current_room"] == "east_room"


def test_movement_handler_move_invalid(setup_test_db):
    """Test that the player cannot move to an invalid direction using MovementHandler."""
    # Given
    player_name = "TestPlayer"
    PlayerModel.create_player(setup_test_db, name=player_name)
    movement_handler = MovementHandler()

    # When - Player tries to move north (which is not available)
    result = movement_handler.move_player(setup_test_db, player_name, "north")

    # Then
    assert result["success"] is False
    assert result["message"] == "You can't move in that direction."
    player = PlayerModel.get_player_by_name(setup_test_db, player_name)
    player_dict = dict(player)  # Convert Row object to dictionary
    assert player_dict["current_room"] == "start"