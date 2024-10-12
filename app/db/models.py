# Define the player model and related database operations
class PlayerModel:

    @staticmethod
    def create_table(connection):
        """Create the players table if it doesn't exist."""
        with connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS players (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    current_room TEXT NOT NULL
                );
            """)

    @staticmethod
    def create_player(connection, name: str, current_room: str = "start"):
        """Insert a new player into the database."""
        with connection:
            connection.execute("""
                INSERT INTO players (name, current_room)
                VALUES (?, ?);
            """, (name, current_room))

    @staticmethod
    def get_player_by_name(connection, name: str):
        """Retrieve a player by name."""
        player = connection.execute("""
            SELECT * FROM players WHERE name = ?;
        """, (name,)).fetchone()
        return player

    @staticmethod
    def update_player_location(connection, player_id: int, new_room: str):
        """Update the current room for the player."""
        with connection:
            connection.execute("""
                UPDATE players
                SET current_room = ?
                WHERE id = ?;
            """, (new_room, player_id))

# Example table creation for other entities (items, rooms, etc.)
class RoomModel:

    @staticmethod
    def create_table(connection):
        """Create the rooms table if it doesn't exist."""
        with connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS rooms (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT NOT NULL
                );
            """)

    @staticmethod
    def create_room(connection, name: str, description: str):
        """Insert a new room into the database."""
        with connection:
            connection.execute("""
                INSERT INTO rooms (name, description)
                VALUES (?, ?);
            """, (name, description))

    @staticmethod
    def get_room_by_name(connection, name: str):
        """Retrieve a room by its name."""
        room = connection.execute("""
            SELECT * FROM rooms WHERE name = ?;
        """, (name,)).fetchone()
        return room

