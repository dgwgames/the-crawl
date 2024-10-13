import pytest

from app.core.game_engine import GameEngine
from app.core.inventory_handler import InventoryHandler
from app.core.services.world_generation_service import WorldGenerationService
from app.db.models import PlayerModel, RoomModel, InventoryModel
from app.db.database import get_singleton_db_connection, init_db
import logging
import os

# Ensure the logs directory exists
os.makedirs("logs", exist_ok=True)

# Configure logging to write to both console and file
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Console output
        logging.FileHandler("logs/app.log")  # File output
    ]
)
logger = logging.getLogger(__name__)
logger.info("Logging to both console and file.")


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

    # Drop and recreate tables to ensure schema is up to date
    logger.info("Dropping existing tables if they exist.")
    connection.execute("DROP TABLE IF EXISTS rooms;")
    connection.execute("DROP TABLE IF EXISTS players;")
    connection.execute("DROP TABLE IF EXISTS inventory;")

    # Initialize tables with the updated schema
    logger.info("Creating tables with the updated schema.")
    PlayerModel.create_table(connection)
    RoomModel.create_table(connection)
    InventoryModel.create_table(connection)

    # Clear any existing data to ensure a clean state
    logger.info("Clearing existing data from players, rooms, and inventory tables.")
    connection.execute("DELETE FROM players;")
    connection.execute("DELETE FROM rooms;")
    connection.execute("DELETE FROM inventory;")

    # Create initial rooms with coordinates
    logger.info("Creating initial rooms: 'start', 'east_room', and 'west_room'.")
    RoomModel.create_room(connection, "start", "The starting point of your journey.", 0, 0)
    RoomModel.create_room(connection, "east_room", "You have entered the east room.", 1, 0)
    RoomModel.create_room(connection, "west_room", "You have entered the west room.", -1, 0)

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


@pytest.fixture
def world_service(setup_test_db):
    """
    Fixture to set up the WorldGenerationService with a test database connection.
    """
    return WorldGenerationService(setup_test_db)