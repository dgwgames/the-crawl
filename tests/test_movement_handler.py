import logging
from app.db.models import PlayerModel, InventoryModel
from app.core.movement_handler import MovementHandler
from tests.fixtures import setup_test_db

logger = logging.getLogger(__name__)


def test_movement_handler_move_valid(setup_test_db):
    """Test that a player can successfully move between rooms using MovementHandler."""
    logger.info("Starting test: test_movement_handler_move_valid")
    # Given
    player_name = "TestPlayer"
    logger.info("Creating player with name: %s", player_name)
    PlayerModel.create_player(setup_test_db, name=player_name)
    movement_handler = MovementHandler()

    # When - Player moves east
    logger.info("Player '%s' moves east.", player_name)
    result = movement_handler.move_player(setup_test_db, player_name, "east")

    # Then
    logger.info("Asserting the player has moved to 'east_room'.")
    assert result["success"] is True
    assert result["message"] == "You have moved to the east_room."
    player = PlayerModel.get_player_by_name(setup_test_db, player_name)
    player_dict = dict(player)  # Convert Row object to dictionary
    assert player_dict["current_room"] == "east_room"


def test_movement_handler_move_invalid(setup_test_db):
    """Test that the player cannot move to an invalid direction using MovementHandler."""
    logger.info("Starting test: test_movement_handler_move_invalid")
    # Given
    player_name = "TestPlayer"
    logger.info("Creating player with name: %s", player_name)
    PlayerModel.create_player(setup_test_db, name=player_name)
    movement_handler = MovementHandler()

    # When - Player tries to move north (which is not available)
    logger.info("Player '%s' tries to move north, which is not available.", player_name)
    result = movement_handler.move_player(setup_test_db, player_name, "north")

    # Then
    logger.info("Asserting the player cannot move north.")
    assert result["success"] is False
    assert result["message"] == "You can't move in that direction."
    player = PlayerModel.get_player_by_name(setup_test_db, player_name)
    player_dict = dict(player)  # Convert Row object to dictionary
    assert player_dict["current_room"] == "start"


def test_inventory_interaction_after_movement(setup_test_db):
    """Test that a player can pick up an item from a room and it moves to their inventory."""
    logger.info("Starting test: test_inventory_interaction_after_movement")
    # Given
    player_name = "TestPlayer"
    item_name = "Magic Sword"
    logger.info("Creating player with name: %s and adding item '%s' to room 'east_room'.", player_name, item_name)
    PlayerModel.create_player(setup_test_db, name=player_name)
    InventoryModel.create_table(setup_test_db)
    InventoryModel.add_item_to_room(setup_test_db, room_name="east_room", item_name=item_name)
    movement_handler = MovementHandler()

    # When - Player moves east to the room with the item
    logger.info("Player '%s' moves east to pick up the item '%s'.", player_name, item_name)
    movement_handler.move_player(setup_test_db, player_name, "east")

    # Player picks up the item
    logger.info("Player '%s' picks up the item '%s' from room 'east_room'.", player_name, item_name)
    InventoryModel.remove_item_from_room(setup_test_db, room_name="east_room", item_name=item_name)
    InventoryModel.add_item_to_player(setup_test_db, player_name=player_name, item_name=item_name)

    # Then - Verify item is in player's inventory and not in the room
    logger.info("Asserting the item '%s' is now in the player's inventory and not in the room.", item_name)
    assert InventoryModel.is_item_with_player(setup_test_db, player_name, item_name) is True
    assert InventoryModel.is_item_in_room(setup_test_db, room_name="east_room", item_name=item_name) is False
