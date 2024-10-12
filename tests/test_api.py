import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_register_player_endpoint():
    response = client.post("/api/v1/player/register", json={"name": "TestPlayer"})
    assert response.status_code == 200
    assert response.json()["message"] == "Player 'TestPlayer' has been registered."


def test_move_player_endpoint():
    # First, register the player
    client.post("/api/v1/player/register", json={"name": "TestPlayer"})

    # Then, attempt to move the player
    response = client.post("/api/v1/player/move", json={"player_name": "TestPlayer", "direction": "east"})
    assert response.status_code == 200
    assert "message" in response.json()
