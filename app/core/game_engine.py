from app.core.movement_handler import MovementHandler

class GameEngine:
    def __init__(self):
        self.movement_handler = MovementHandler()

    def move(self, connection, player_name: str, direction: str):
        """Delegates the move request to the MovementHandler."""
        return self.movement_handler.move_player(connection, player_name, direction)
