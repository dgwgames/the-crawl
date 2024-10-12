import pytest
import logging
from app.core.game_engine import GameEngine
from app.db.models import PlayerModel
from tests.fixtures import setup_test_db

logger = logging.getLogger(__name__)


@pytest.fixture
def game_engine():
    """Provides an instance of GameEngine for testing."""
    logger.info("Creating an instance of GameEngine for testing.")
    return GameEngine()


def test_move_to_east(game_engine, setup_test_db):
    logger.info("Starting test: test_move_to_east")
    # Setup - Add a player
    player_name = "TestPlayer"
    logger.info("Creating player with name: %s", player_name)
    PlayerModel.create_player(setup_test_db, name=player_name)

    # When - Move player to the east
    logger.info("Moving player '%s' to the east.", player_name)
    result = game_engine.move(setup_test_db, player_name, "east")

    # Then
    logger.info("Asserting the player has moved to 'east_room'.")
    assert result["success"] is True
    assert result["message"] == "You have moved to east_room."

    # Verify the player's current room in the database
    player = PlayerModel.get_player_by_name(setup_test_db, player_name)
    player_dict = dict(player)  # Convert Row object to dictionary
    assert player_dict["current_room"] == "east_room"
