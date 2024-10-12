from fastapi.testclient import TestClient
from app.main import app
from app.db.models import PlayerModel, RoomModel
from app.db.database import init_db, get_singleton_db_connection

client = TestClient(app)

# Initialize the database before running tests
init_db()


def setup_rooms():
    connection = get_singleton_db_connection()
    RoomModel.create_table(connection)
    RoomModel.create_room(connection, "start", "The starting room.")
    RoomModel.create_room(connection, "east_room", "A room to the east.")


def test_move_player_endpoint():
    # Set up the initial state using the singleton connection
    connection = get_singleton_db_connection()
    setup_rooms()
    PlayerModel.create_table(connection)
    PlayerModel.create_player(connection, name="TestPlayer")

    # Use the FastAPI client to perform the endpoint tests
    response = client.post("/api/v1/player/register", json={"name": "TestPlayer"})
    assert response.status_code == 200
    assert response.json()["message"] == "Player 'TestPlayer' has been registered."

    # Then, attempt to move the player
    response = client.post("/api/v1/player/move", json={"player_name": "TestPlayer", "direction": "east"})
    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json()["message"] == "You have moved to east_room."
