import pytest
import sqlite3
from app.db.models import PlayerModel, RoomModel, InventoryModel
from app.core.inventory_handler import InventoryHandler


@pytest.fixture(scope="function")
def setup_test_db():
    """Sets up a temporary in-memory SQLite database for testing."""
    connection = sqlite3.connect(":memory:")
    connection.row_factory = sqlite3.Row

    # Create tables for players, rooms, and inventory
    PlayerModel.create_table(connection)
    RoomModel.create_table(connection)
    InventoryModel.create_table(connection)

    # Add a room
    RoomModel.create_room(connection, "start", "The starting point of your journey.")

    yield connection

    connection.close()


@pytest.fixture
def inventory_handler():
    """Provides an instance of InventoryHandler for testing."""
    return InventoryHandler()


def test_pick_up_item(setup_test_db, inventory_handler):
    """Test that a player can pick up an item."""
    # Setup - Add player and item to room
    player_name = "TestPlayer"
    PlayerModel.create_player(setup_test_db, name=player_name)
    item_name = "Magic Sword"
    InventoryModel.add_item_to_room(setup_test_db, "start", item_name)

    # When - Player picks up the item
    result = inventory_handler.pick_up_item(setup_test_db, player_name, item_name)

    # Then
    assert result["success"] is True
    assert result["message"] == f"{item_name} has been picked up."
    inventory = InventoryModel.get_player_inventory(setup_test_db, player_name)
    assert item_name in inventory


def test_drop_item(setup_test_db, inventory_handler):
    """Test that a player can drop an item."""
    # Setup - Add player and give them an item
    player_name = "TestPlayer"
    PlayerModel.create_player(setup_test_db, name=player_name)
    item_name = "Magic Sword"
    InventoryModel.add_item_to_player(setup_test_db, player_name, item_name)

    # When - Player drops the item
    result = inventory_handler.drop_item(setup_test_db, player_name, item_name)

    # Then
    assert result["success"] is True
    assert result["message"] == f"{item_name} has been dropped."
    inventory = InventoryModel.get_player_inventory(setup_test_db, player_name)
    assert item_name not in inventory


def test_view_inventory(setup_test_db, inventory_handler):
    """Test that a player can view their inventory."""
    # Setup - Add player and give them items
    player_name = "TestPlayer"
    PlayerModel.create_player(setup_test_db, name=player_name)
    items = ["Magic Sword", "Healing Potion"]
    for item in items:
        InventoryModel.add_item_to_player(setup_test_db, player_name, item)

    # When - Player views their inventory
    inventory = inventory_handler.view_inventory(setup_test_db, player_name)

    # Then
    assert len(inventory) == 2
    assert "Magic Sword" in inventory
    assert "Healing Potion" in inventory
