import pytest
from app.api.v1.player import register_player
from app.api.v1.player import PlayerRegistration  # Import the Pydantic model


@pytest.mark.asyncio
async def test_register_player():
    # Mock input
    player_data = PlayerRegistration(name="TestPlayer")

    # Call the function (await since it's async)
    result = await register_player(player=player_data)

    # Assert the response is correct
    assert result["message"] == f"Player '{player_data.name}' has been registered."
