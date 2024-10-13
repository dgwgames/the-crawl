import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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


class RoomModel:
    @staticmethod
    def create_table(connection):
        """Create the rooms table if it doesn't exist."""
        with connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS rooms (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT NOT NULL,
                    x_coordinate INTEGER NOT NULL,
                    y_coordinate INTEGER NOT NULL
                );
            """)

    @staticmethod
    def create_room(connection, name: str, description: str, x_coordinate: int, y_coordinate: int):
        """Insert a new room into the database."""
        with connection:
            connection.execute("""
                INSERT INTO rooms (name, description, x_coordinate, y_coordinate)
                VALUES (?, ?, ?, ?);
            """, (name, description, x_coordinate, y_coordinate))

    @staticmethod
    def get_room_by_coordinates(connection, coordinates: dict):
        """Retrieve a room by its coordinates."""
        room = connection.execute("""
            SELECT * FROM rooms WHERE x_coordinate = ? AND y_coordinate = ?;
        """, (coordinates['x'], coordinates['y'])).fetchone()
        return room


class InventoryModel:
    @staticmethod
    def create_table(connection):
        """Create the inventory table."""
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
        connection.execute("""
            INSERT INTO inventory (room_name, item_name)
            VALUES (?, ?);
        """, (room_name, item_name))

    @staticmethod
    def add_item_to_player(connection, player_name: str, item_name: str):
        """Add an item to a player's inventory."""
        connection.execute("""
            INSERT INTO inventory (player_name, item_name)
            VALUES (?, ?);
        """, (player_name, item_name))

    @staticmethod
    def remove_item_from_room(connection, room_name: str, item_name: str):
        """Remove an item from a room."""
        connection.execute("""
            DELETE FROM inventory WHERE room_name = ? AND item_name = ?;
        """, (room_name, item_name))

    @staticmethod
    def remove_item_from_player(connection, player_name: str, item_name: str):
        """Remove an item from a player's inventory."""
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


class NeighborRelationModel:
    @staticmethod
    def create_table(connection):
        """Create the neighbor_relations table if it doesn't exist."""
        connection.execute("""
            CREATE TABLE IF NOT EXISTS neighbor_relations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                room_id INTEGER NOT NULL,
                neighbor_room_id INTEGER NOT NULL,
                direction TEXT NOT NULL,
                FOREIGN KEY(room_id) REFERENCES rooms(id),
                FOREIGN KEY(neighbor_room_id) REFERENCES rooms(id)
            );
        """)

    @staticmethod
    def add_neighbor_relation(connection, room_id: int, neighbor_room_id: int, direction: str):
        """Create a relation between two neighboring rooms with a direction."""
        connection.execute("""
            INSERT INTO neighbor_relations (room_id, neighbor_room_id, direction)
            VALUES (?, ?, ?);
        """, (room_id, neighbor_room_id, direction))

    @staticmethod
    def get_neighbors(connection, room_id: int):
        """Retrieve all neighboring rooms of a specific room."""
        neighbors = connection.execute("""
            SELECT neighbor_room_id FROM neighbor_relations WHERE room_id = ?;
        """, (room_id,)).fetchall()
        return [neighbor["neighbor_room_id"] for neighbor in neighbors]
