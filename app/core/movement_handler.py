from app.db.models import PlayerModel

class MovementHandler:
    def __init__(self):
        # Define valid movements from each room
        self.room_transitions = {
            "start": {"east": "east_room", "west": "west_room"},
            "east_room": {"west": "start"},
            "west_room": {"east": "start"}
        }

    def move_player(self, connection, player_name: str, direction: str):
        """Handles player movement."""
        # Retrieve player data
        player = PlayerModel.get_player_by_name(connection, player_name)
        if not player:
            return {"success": False, "message": "Player not found."}

        current_room = player["current_room"]

        # Determine the target room based on direction
        if direction in self.room_transitions.get(current_room, {}):
            new_room = self.room_transitions[current_room][direction]
            PlayerModel.update_player_location(connection, player["id"], new_room)
            return {"success": True, "message": f"You have moved to the {new_room}."}
        else:
            return {"success": False, "message": "You can't move in that direction."}
