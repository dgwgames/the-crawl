# Updated to use the singleton pattern with unique constraint on room coordinates

from app.db.singleton_db import get_singleton_db_connection


def get_connection():
    connection = get_singleton_db_connection()
    try:
        yield connection
    finally:
        # Do not close the singleton connection here, it should be shared.
        pass


def init_db():
    connection = get_singleton_db_connection()
    with connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                current_room TEXT NOT NULL
            );
        """)
        connection.execute("""
            CREATE TABLE IF NOT EXISTS rooms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                x_coordinate INTEGER NOT NULL,
                y_coordinate INTEGER NOT NULL,
                UNIQUE (x_coordinate, y_coordinate)  -- Adding unique constraint for coordinates
            );
        """)
