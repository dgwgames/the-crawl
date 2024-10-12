import logging

from app.core.movement_handler import MovementHandler
from app.db.models import PlayerModel


class GameEngine:
    def __init__(self):
        self.movement_handler = MovementHandler()

    def move(self, connection, player_name: str, direction: str) -> dict:
        """Handles player movement in a specified direction."""
        # Retrieve player data
        player = PlayerModel.get_player_by_name(connection, player_name)

        if not player:
            return {"success": False, "message": f"Player '{player_name}' not found."}

        current_room = player["current_room"]
        logging.debug(f"Current room for player '{player_name}': {current_room}")

        # Example updated logic for allowed moves
        valid_moves = {
            "start": {"east": "east_room"},
            "east_room": {"west": "start"}
        }

        # Check if movement is possible
        if current_room not in valid_moves or direction not in valid_moves[current_room]:
            logging.error(f"Failed to move player '{player_name}': You can't move in that direction.")
            return {"success": False, "message": "You can't move in that direction."}

        # Determine the new room and update player's location
        new_room = valid_moves[current_room][direction]
        PlayerModel.update_player_location(connection, player_name, new_room)
        logging.debug(f"Player '{player_name}' moved to new room: {new_room}")

        return {"success": True, "message": f"You have moved to {new_room}."}