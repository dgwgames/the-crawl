from app.db.models import InventoryModel, PlayerModel


class InventoryHandler:

    def pick_up_item(self, connection, player_name: str, item_name: str):
        """Handles player picking up an item."""
        # Check if player exists
        player = PlayerModel.get_player_by_name(connection, player_name)
        if not player:
            return {"success": False, "message": "Player not found."}

        # Check if item is in the room
        current_room = player["current_room"]
        if not InventoryModel.is_item_in_room(connection, current_room, item_name):
            return {"success": False, "message": f"{item_name} is not in the room."}

        # Add item to player's inventory
        InventoryModel.add_item_to_player(connection, player_name, item_name)
        InventoryModel.remove_item_from_room(connection, current_room, item_name)

        return {"success": True, "message": f"{item_name} has been picked up."}

    def drop_item(self, connection, player_name: str, item_name: str):
        """Handles player dropping an item."""
        # Check if player exists
        player = PlayerModel.get_player_by_name(connection, player_name)
        if not player:
            return {"success": False, "message": "Player not found."}

        # Check if player has the item
        if not InventoryModel.is_item_with_player(connection, player_name, item_name):
            return {"success": False, "message": f"{item_name} is not in your inventory."}

        # Remove item from player's inventory and add to room
        InventoryModel.remove_item_from_player(connection, player_name, item_name)
        current_room = player["current_room"]
        InventoryModel.add_item_to_room(connection, current_room, item_name)

        return {"success": True, "message": f"{item_name} has been dropped."}

    def view_inventory(self, connection, player_name: str):
        """Returns the player's inventory."""
        return InventoryModel.get_player_inventory(connection, player_name)
