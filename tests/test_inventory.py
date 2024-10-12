import logging
from app.db.models import PlayerModel, InventoryModel
from tests.fixtures import setup_test_db, inventory_handler

logger = logging.getLogger(__name__)


def test_pick_up_item(setup_test_db, inventory_handler):
    """Test that a player can pick up an item."""
    logger.info("Starting test: test_pick_up_item")
    # Setup - Add player and item to room
    player_name = "TestPlayer"
    item_name = "Magic Sword"
    logger.info("Creating player with name: %s and adding item '%s' to room 'start'.", player_name, item_name)
    PlayerModel.create_player(setup_test_db, name=player_name)
    InventoryModel.add_item_to_room(setup_test_db, "start", item_name)

    # When - Player picks up the item
    logger.info("Player '%s' picks up the item '%s'.", player_name, item_name)
    result = inventory_handler.pick_up_item(setup_test_db, player_name, item_name)

    # Then
    logger.info("Asserting the item has been picked up by the player.")
    assert result["success"] is True
    assert result["message"] == f"{item_name} has been picked up."
    inventory = InventoryModel.get_player_inventory(setup_test_db, player_name)
    assert item_name in inventory


def test_drop_item(setup_test_db, inventory_handler):
    """Test that a player can drop an item."""
    logger.info("Starting test: test_drop_item")
    # Setup - Add player and give them an item
    player_name = "TestPlayer"
    item_name = "Magic Sword"
    logger.info("Creating player with name: %s and giving them item '%s'.", player_name, item_name)
    PlayerModel.create_player(setup_test_db, name=player_name)
    InventoryModel.add_item_to_player(setup_test_db, player_name, item_name)

    # When - Player drops the item
    logger.info("Player '%s' drops the item '%s'.", player_name, item_name)
    result = inventory_handler.drop_item(setup_test_db, player_name, item_name)

    # Then
    logger.info("Asserting the item has been dropped by the player.")
    assert result["success"] is True
    assert result["message"] == f"{item_name} has been dropped."
    inventory = InventoryModel.get_player_inventory(setup_test_db, player_name)
    assert item_name not in inventory


def test_view_inventory(setup_test_db, inventory_handler):
    """Test that a player can view their inventory."""
    logger.info("Starting test: test_view_inventory")
    # Setup - Add player and give them items
    player_name = "TestPlayer"
    items = ["Magic Sword", "Healing Potion"]
    logger.info("Creating player with name: %s and giving them items: %s", player_name, items)
    PlayerModel.create_player(setup_test_db, name=player_name)
    for item in items:
        InventoryModel.add_item_to_player(setup_test_db, player_name, item)

    # When - Player views their inventory
    logger.info("Player '%s' views their inventory.", player_name)
    inventory = inventory_handler.view_inventory(setup_test_db, player_name)

    # Then
    logger.info("Asserting the player's inventory contains the correct items.")
    assert len(inventory) == 2
    assert "Magic Sword" in inventory
    assert "Healing Potion" in inventory
