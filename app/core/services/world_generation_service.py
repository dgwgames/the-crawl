import logging
from app.core.gpt_service import get_gpt_response
from app.db.models import RoomModel, NeighborRelationModel

logger = logging.getLogger(__name__)


class WorldGenerationService:
    def __init__(self, connection):
        self.connection = connection

    async def generate_map_room(self, prompt: str):
        try:
            # Call the GPT service to generate a room
            data = await get_gpt_response(prompt)

            # Check if the response contains the expected data
            if "name" not in data or "description" not in data:
                raise ValueError(f"Unexpected response from GPT: {data}")

            return {
                "name": data["name"],
                "description": data["description"],
                "grid_coordinates": data.get("grid_coordinates", {"x": 0, "y": 0})
            }
        except Exception as e:
            logger.error(f"Error while generating map room: {str(e)}")
            return {"error": f"Error while generating map room: {str(e)}"}

    def save_map_room_to_db(self, room_data: dict):
        """
        Save the generated map room to the database.

        :param room_data: The dictionary containing room details (name, description, coordinates).
        """
        try:
            logger.info(f"Saving map room to database: {room_data}")
            name = room_data.get("name")
            description = room_data.get("description")
            coordinates = room_data.get("grid_coordinates")

            # Extract x and y coordinates from the grid_coordinates dict
            x_coordinate = coordinates.get('x')
            y_coordinate = coordinates.get('y')

            RoomModel.create_room(self.connection, name, description, x_coordinate, y_coordinate)
        except Exception as e:
            logger.error(f"Error while saving map room to database: {str(e)}")

    def connect_rooms(self, room_a_id, room_b_id, direction):
        """
        Create a neighboring relationship between two rooms.

        :param room_a_id: ID of the first room.
        :param room_b_id: ID of the neighboring room.
        :param direction: The direction connecting from room A to room B (e.g., "north", "east").
        """
        try:
            logger.info(f"Connecting rooms {room_a_id} to {room_b_id} via {direction}")
            NeighborRelationModel.create_relation(self.connection, room_a_id, room_b_id, direction)
        except Exception as e:
            logger.error(f"Error while creating neighboring relation: {str(e)}")

    def get_existing_room(self, coordinates):
        """
        Retrieve an existing room based on coordinates.

        :param coordinates: The grid coordinates to look up the room.
        :return: The room if found, else None.
        """
        return RoomModel.get_room_by_coordinates(self.connection, coordinates)

    async def generate_connected_room(self, current_coordinates, direction):
        """
        Generate a new room connected to an existing room in the given direction.

        :param current_coordinates: The coordinates of the current room.
        :param direction: The direction in which to generate the connected room.
        :return: The generated room data.
        """
        # Retrieve current room from coordinates
        current_room = self.get_existing_room(current_coordinates)
        if not current_room:
            return {"error": "Current room not found."}

        # Prepare GPT prompt with current coordinates and direction
        prompt = f"""
        Generate a map location for a grid-based text game. 
        The response should be a JSON object with the following structure:
        {{
          "origin_location_coordinates": {{"x": {current_coordinates['x']}, "y": {current_coordinates['y']}}},
          "direction_from_origin_location": "{direction}",
          "new_location_coordinates": {{"x": "new x location", "y": "new y location"}},
          "new_location_name": "provide a fictional location Name",
          "new_description": "A detailed description of the location.",
          "new_location_type": "outdoor: edge of a forest",
          "new_location_features": [
            {{"type": "feature type", "description": "A description of the feature"}}
          ],
          "new_location_sounds": ["list of sounds"],
          "new_location_smells": ["list of smells"]
        }}
        Ensure the response is strictly in this format.
        """

        # Generate a new room using GPT
        new_room_data = await get_gpt_response(prompt)

        if "new_location_coordinates" not in new_room_data or "new_location_name" not in new_room_data:
            return {"error": "Incomplete room data returned by GPT."}

        """
        # Save the new room to the database
        self.save_map_room_to_db(new_room_data)

        # Retrieve the new room by its coordinates
        new_room = self.get_existing_room(new_room_data['new_location_coordinates'])
        if not new_room:
            return {"error": "Failed to retrieve the newly created room."}
        
        # Create relationship in the database
        self.connect_rooms(current_room['id'], new_room['id'], direction)

        # Reverse connection (e.g., east -> west)
        reverse_directions = {
            "north": "south",
            "south": "north",
            "east": "west",
            "west": "east"
        }
        reverse_direction = reverse_directions.get(direction)
        if reverse_direction:
            self.connect_rooms(new_room['id'], current_room['id'], reverse_direction)
        """
        # Return the new room data
        return new_room_data
