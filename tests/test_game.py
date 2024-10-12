import pytest
import sqlite3
from app.core.game_engine import GameEngine
from app.db.models import PlayerModel, RoomModel


@pytest.fixture(scope="function")
def setup_test_db():
    """Sets up a temporary in-memory SQLite database for testing."""
    connection = sqlite3.connect(":memory:")
    connection.row_factory = sqlite3.Row

    # Create tables for players and rooms
    PlayerModel.create_table(connection)
    RoomModel.create_table(connection)

    # Create initial rooms
    RoomModel.create_room(connection, "start", "The starting point of your journey.")
    RoomModel.create_room(connection, "east_room", "A room to the east.")

    yield connection
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
    assert result["success"] is True
    assert result["message"] == "You have moved to east_room."

    # Verify the player's current room in the database
    player = PlayerModel.get_player_by_name(setup_test_db, player_name)
    player_dict = dict(player)  # Convert Row object to dictionary
    assert player_dict["current_room"] == "east_room"
