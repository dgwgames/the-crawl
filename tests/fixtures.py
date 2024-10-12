import pytest

from app.core.game_engine import GameEngine
from app.core.inventory_handler import InventoryHandler
from app.db.models import PlayerModel, RoomModel, InventoryModel
from app.db.database import get_singleton_db_connection, init_db
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@pytest.fixture
def game_engine():
    """Provides an instance of GameEngine for testing."""
    logger.info("Creating an instance of GameEngine for testing.")
    return GameEngine()


@pytest.fixture(scope="function")
def setup_test_db():
    """Sets up a persistent SQLite database for testing using the singleton connection."""
    logger.info("Setting up a persistent SQLite database for testing using the singleton connection.")
    connection = get_singleton_db_connection()

    # Initialize tables if they do not exist
    init_db()
    PlayerModel.create_table(connection)
    RoomModel.create_table(connection)
    InventoryModel.create_table(connection)

    # Clear any existing data to ensure a clean state
    logger.info("Clearing existing data from players, rooms, and inventory tables.")
    connection.execute("DELETE FROM players;")
    connection.execute("DELETE FROM rooms;")
    connection.execute("DELETE FROM inventory;")

    # Create initial rooms
    logger.info("Creating initial rooms: 'start', 'east_room', and 'west_room'.")
    RoomModel.create_room(connection, "start", "The starting point of your journey.")
    RoomModel.create_room(connection, "east_room", "You have entered the east room.")
    RoomModel.create_room(connection, "west_room", "You have entered the west room.")

    yield connection  # Provide the connection to the test function

    # Teardown: Clear data after each test to maintain isolation
    logger.info("Clearing data from players, rooms, and inventory tables after test completion.")
    connection.execute("DELETE FROM players;")
    connection.execute("DELETE FROM rooms;")
    connection.execute("DELETE FROM inventory;")


@pytest.fixture
def inventory_handler():
    """Provides an instance of InventoryHandler for testing."""
    logger.info("Creating an instance of InventoryHandler for testing.")
    return InventoryHandler()
