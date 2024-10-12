import logging

from app.api.v1.player import PlayerRegistration
from app.api.v1.player import register_player  # Import the Pydantic model

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def register_test_player(connection, player_name="TestPlayer"):
    """Helper function to register a player for testing."""
    player_data = PlayerRegistration(name=player_name)
    logger.info("Registering player with name: %s", player_data.name)
    return await register_player(player=player_data, connection=connection)


