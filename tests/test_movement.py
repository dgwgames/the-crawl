import pytest
import sqlite3
from app.core.game_engine import GameEngine
from app.db.models import PlayerModel, RoomModel

# Test fixtures help set up and tear down a temporary database for testing
@pytest.fixture(scope="function")
def setup_test_db():
    """Sets up a temporary in-memory SQLite database for testing."""
    # Use an in-memory SQLite database for testing
    connection = sqlite3.connect(":memory:")
    connection.row_factory = sqlite3.Row

    # Create tables
    PlayerModel.create_table(connection)
    RoomModel.create_table(connection)

    # Create initial rooms
    RoomModel.create_room(connection, "start", "The starting point of your journey.")
    RoomModel.create_room(connection, "east_room", "You have entered the east room.")
    RoomModel.create_room(connection, "west_room", "You have entered the west room.")

    yield connection  # Provide the connection to the test function

    # Teardown: Close the connection
    connection.close()

def test_player_move_valid(setup_test_db):
    """Test that a player can successfully move between rooms."""
    # Given
    player_name = "TestPlayer"
    PlayerModel.create_player(setup_test_db, name=player_name)
    game_engine = GameEngine()

    # When - Player moves east
    result = game_engine.move(setup_test_db, player_name, "east")

    # Then
    assert result["success"] is True
    assert "You have moved to" in result["message"]
    assert "east_room" in result["message"]
    player = PlayerModel.get_player_by_name(setup_test_db, player_name)
    assert player["current_room"] == "east_room"

def test_player_move_invalid(setup_test_db):
    """Test that the player cannot move to an invalid direction."""
    # Given
    player_name = "TestPlayer"
    PlayerModel.create_player(setup_test_db, name=player_name)
    game_engine = GameEngine()

    # When - Player tries to move north (which is not available)
    result = game_engine.move(setup_test_db, player_name, "north")

    # Then
    assert result["success"] is False
    assert result["message"] == "You can't move in that direction."
    player = PlayerModel.get_player_by_name(setup_test_db, player_name)
    assert player["current_room"] == "start"
