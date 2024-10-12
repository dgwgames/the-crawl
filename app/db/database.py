import sqlite3

DATABASE_URL = "dungeon_crawler.db"

def get_db_connection():
    connection = sqlite3.connect(DATABASE_URL)
    connection.row_factory = sqlite3.Row
    return connection

def init_db():
    connection = get_db_connection()
    with connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                current_room TEXT NOT NULL
            );
        """)
