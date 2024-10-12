# Define the player model and related database operations
class PlayerModel:

    @staticmethod
    def create_table(connection):
        """Create the players table if it doesn't exist."""
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
    def update_player_location(connection, player_name: str, new_room: str):
        """Update a player's current room."""
        connection.execute("""
            UPDATE players SET current_room = ? WHERE name = ?;
        """, (new_room, player_name))


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


class InventoryModel:

    @staticmethod
    def create_table(connection):
        """Create the inventory table."""
        with connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS inventory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    player_name TEXT,
                    room_name TEXT,
                    item_name TEXT,
                    FOREIGN KEY(player_name) REFERENCES players(name),
                    FOREIGN KEY(room_name) REFERENCES rooms(name)
                );
            """)

    @staticmethod
    def add_item_to_room(connection, room_name: str, item_name: str):
        """Add an item to a room."""
        with connection:
            connection.execute("""
                INSERT INTO inventory (room_name, item_name)
                VALUES (?, ?);
            """, (room_name, item_name))

    @staticmethod
    def add_item_to_player(connection, player_name: str, item_name: str):
        """Add an item to a player's inventory."""
        with connection:
            connection.execute("""
                INSERT INTO inventory (player_name, item_name)
                VALUES (?, ?);
            """, (player_name, item_name))

    @staticmethod
    def remove_item_from_room(connection, room_name: str, item_name: str):
        """Remove an item from a room."""
        with connection:
            connection.execute("""
                DELETE FROM inventory WHERE room_name = ? AND item_name = ?;
            """, (room_name, item_name))

    @staticmethod
    def remove_item_from_player(connection, player_name: str, item_name: str):
        """Remove an item from a player's inventory."""
        with connection:
            connection.execute("""
                DELETE FROM inventory WHERE player_name = ? AND item_name = ?;
            """, (player_name, item_name))

    @staticmethod
    def is_item_in_room(connection, room_name: str, item_name: str) -> bool:
        """Check if an item is in the room."""
        item = connection.execute("""
            SELECT * FROM inventory WHERE room_name = ? AND item_name = ?;
        """, (room_name, item_name)).fetchone()
        return item is not None

    @staticmethod
    def is_item_with_player(connection, player_name: str, item_name: str) -> bool:
        """Check if an item is with the player."""
        item = connection.execute("""
            SELECT * FROM inventory WHERE player_name = ? AND item_name = ?;
        """, (player_name, item_name)).fetchone()
        return item is not None

    @staticmethod
    def get_player_inventory(connection, player_name: str):
        """Get all items in a player's inventory."""
        items = connection.execute("""
            SELECT item_name FROM inventory WHERE player_name = ?;
        """, (player_name,)).fetchall()
        return [item["item_name"] for item in items]