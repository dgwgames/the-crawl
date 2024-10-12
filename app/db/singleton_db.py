# app/db/singleton_db.py

import sqlite3
import threading


class SingletonDB:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(SingletonDB, cls).__new__(cls)
                    cls._instance._connection = sqlite3.connect("singleton_dungeon_crawler.db", check_same_thread=False)
                    cls._instance._connection.row_factory = sqlite3.Row
        return cls._instance

    @property
    def connection(self):
        return self._connection


# Accessing the singleton instance
def get_singleton_db_connection():
    return SingletonDB().connection
