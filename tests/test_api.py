import pytest
import logging
from app.db.models import PlayerModel, RoomModel, InventoryModel
from app.core.movement_handler import MovementHandler
from tests.test_utils import register_test_player  # Import from tests.test_utils
from tests.fixtures import setup_test_db

logger = logging.getLogger(__name__)


def test_movement_handler_move_valid(setup_test_db):
    logger.info("Starting test: test_movement_handler_move_valid")
    """Test that a player can successfully move between rooms using MovementHandler."""
    # Given
    player_name = "TestPlayer"
    PlayerModel.create_player(setup_test_db, name=player_name)
    movement_handler = MovementHandler()

    logger.info("Attempting to move player east.")
    # When - Player moves east
    result = movement_handler.move_player(setup_test_db, player_name, "east")

    logger.info("Asserting results.")
    # Then
    assert result["success"] is True
    assert result["message"] == "You have moved to the east_room."
    player = PlayerModel.get_player_by_name(setup_test_db, player_name)
    player_dict = dict(player)  # Convert Row object to dictionary
    assert player_dict["current_room"] == "east_room"


def test_movement_handler_move_invalid(setup_test_db):
    logger.info("Starting test: test_movement_handler_move_invalid")
    """Test that the player cannot move to an invalid direction using MovementHandler."""
    # Given
    player_name = "TestPlayer"
    PlayerModel.create_player(setup_test_db, name=player_name)
    movement_handler = MovementHandler()

    logger.info("Attempting to move player north (invalid direction).")
    # When - Player tries to move north (which is not available)
    result = movement_handler.move_player(setup_test_db, player_name, "north")

    logger.info("Asserting results.")
    # Then
    assert result["success"] is False
    assert result["message"] == "You can't move in that direction."
    player = PlayerModel.get_player_by_name(setup_test_db, player_name)
    player_dict = dict(player)  # Convert Row object to dictionary
    assert player_dict["current_room"] == "start"


@pytest.mark.asyncio
async def test_register_player(setup_test_db):
    """Test registering a player using the persistent connection."""
    logger.info("Starting test: test_register_player")

    # Use the helper function to register a player
    result = await register_test_player(setup_test_db, player_name="TestPlayer")

    # Assert the response is correct
    logger.info("Asserting the player has been registered correctly.")
    assert result["message"] == f"Player 'TestPlayer' has been registered."


def test_inventory_interaction_after_movement(setup_test_db):
    logger.info("Starting test: test_inventory_interaction_after_movement")
    """Test that a player can pick up an item from a room and it moves to their inventory."""
    # Given
    player_name = "TestPlayer"
    item_name = "Magic Sword"
    PlayerModel.create_player(setup_test_db, name=player_name)
    InventoryModel.create_table(setup_test_db)
    InventoryModel.add_item_to_room(setup_test_db, room_name="east_room", item_name=item_name)
    movement_handler = MovementHandler()

    logger.info("Player moving east to the room with the item.")
    # When - Player moves east to the room with the item
    movement_handler.move_player(setup_test_db, player_name, "east")

    logger.info("Player picking up the item.")
    # Player picks up the item
    InventoryModel.remove_item_from_room(setup_test_db, room_name="east_room", item_name=item_name)
    InventoryModel.add_item_to_player(setup_test_db, player_name=player_name, item_name=item_name)

    logger.info("Asserting item is in player's inventory and not in the room.")
    # Then - Verify item is in player's inventory and not in the room
    assert InventoryModel.is_item_with_player(setup_test_db, player_name, item_name) is True
    assert InventoryModel.is_item_in_room(setup_test_db, room_name="east_room", item_name=item_name) is False
