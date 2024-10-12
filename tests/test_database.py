import pytest
import sqlite3
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

    yield connection  # Provide the connection to the test function

    # Teardown: Close the connection
    connection.close()


def test_create_player(setup_test_db):
    """Test inserting a new player into the database."""
    # Given
    player_name = "TestPlayer"

    # When
    PlayerModel.create_player(setup_test_db, name=player_name)

    # Then
    player = setup_test_db.execute("SELECT * FROM players WHERE name = ?", (player_name,)).fetchone()
    assert player is not None
    assert player["name"] == player_name
    assert player["current_room"] == "start"


def test_update_player_location(setup_test_db):
    """Test updating a player's current room."""
    # Given
    player_name = "TestPlayer"
    PlayerModel.create_player(setup_test_db, name=player_name)
    player = setup_test_db.execute("SELECT * FROM players WHERE name = ?", (player_name,)).fetchone()

    # When
    PlayerModel.update_player_location(setup_test_db, player_id=player["id"], new_room="east_room")

    # Then
    updated_player = setup_test_db.execute("SELECT * FROM players WHERE id = ?", (player["id"],)).fetchone()
    assert updated_player["current_room"] == "east_room"


def test_create_room(setup_test_db):
    """Test inserting a new room into the database."""
    # Given
    room_name = "TreasureRoom"
    room_description = "A room filled with treasure."

    # When
    RoomModel.create_room(setup_test_db, name=room_name, description=room_description)

    # Then
    room = setup_test_db.execute("SELECT * FROM rooms WHERE name = ?", (room_name,)).fetchone()
    assert room is not None
    assert room["name"] == room_name
    assert room["description"] == room_description


def test_get_room_by_name(setup_test_db):
    """Test retrieving a room by its name."""
    # Given
    room_name = "HiddenChamber"
    room_description = "A secret room hidden behind a false wall."
    RoomModel.create_room(setup_test_db, name=room_name, description=room_description)

    # When
    room = RoomModel.get_room_by_name(setup_test_db, name=room_name)

    # Then
    assert room is not None
    assert room["name"] == room_name
    assert room["description"] == room_description
