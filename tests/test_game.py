import pytest
import sqlite3
from app.db.models import PlayerModel
from app.core.game_engine import GameEngine


# Test fixtures help set up and tear down a temporary database for testing
@pytest.fixture(scope="function")
def setup_test_db():
    """Sets up a temporary in-memory SQLite database for testing."""
    # Use an in-memory SQLite database for testing
    connection = sqlite3.connect(":memory:")
    connection.row_factory = sqlite3.Row

    # Create tables
    PlayerModel.create_table(connection)

    yield connection  # Provide the connection to the test function

    # Teardown: Close the connection
    connection.close()


@pytest.fixture
def game_engine():
    """Provides an instance of GameEngine for testing."""
    return GameEngine()


def test_move_to_east(game_engine, setup_test_db):
    # Setup - Add a player
    player_name = "TestPlayer"
    PlayerModel.create_player(setup_test_db, name=player_name)

    # When - Move player to the east
    result = game_engine.move(setup_test_db, player_name, "east")

    # Then
    player = PlayerModel.get_player_by_name(setup_test_db, player_name)
    assert player["current_room"] == "east_room"
    assert result["success"] is True
    assert result["message"] == "You have moved to the east_room."


def test_invalid_direction(game_engine, setup_test_db):
    # Setup - Add a player
    player_name = "TestPlayer"
    PlayerModel.create_player(setup_test_db, name=player_name)

    # When - Player attempts invalid move
    result = game_engine.move(setup_test_db, player_name, "north")

    # Then
    assert result["success"] is False
    assert result["message"] == "You can't move in that direction."
