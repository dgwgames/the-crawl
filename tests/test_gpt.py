import pytest
import logging
from fastapi.testclient import TestClient

from app.api.v1.gpt_interaction import router

logger = logging.getLogger(__name__)

client = TestClient(router)


@pytest.mark.asyncio
async def test_gpt_interaction_api():
    """Test GPT interaction API endpoint."""
    logger.info("Starting test: test_gpt_interaction_api")

    # Given
    prompt = """
    Generate a response as an NPC in a text-based role-playing game:

    {
      "name": "NPC name",
      "description": "A detailed description of the NPC",
      "demeanor": "The overall demeanor of the NPC",
      "response": "The reply from the NPC"
    }
    Ensure the response is strictly in this JSON format.
    """

    # When
    response = client.post("/gpt_interaction", json={"prompt": prompt})
    result = response.json()

    # Then
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    # Adjust for the response node
    assert "response" in result, f"Expected 'response' in result, got {result}"
    npc_response = result["response"]

    assert isinstance(npc_response, dict), f"Expected 'response' to be a dictionary, got {type(npc_response)}"
    assert "name" in npc_response, f"Expected 'name' in response, got {npc_response}"
    assert "description" in npc_response, f"Expected 'description' in response, got {npc_response}"
    assert "demeanor" in npc_response, f"Expected 'demeanor' in response, got {npc_response}"
    assert "response" in npc_response, f"Expected 'response' in response, got {npc_response}"

    # Optional: Additional type checking
    assert isinstance(npc_response["name"], str), f"Expected 'name' to be a string, got {type(npc_response['name'])}"
    assert isinstance(npc_response["description"],
                      str), f"Expected 'description' to be a string, got {type(npc_response['description'])}"
    assert isinstance(npc_response["demeanor"],
                      str), f"Expected 'demeanor' to be a string, got {type(npc_response['demeanor'])}"
    assert isinstance(npc_response["response"],
                      str), f"Expected 'response' to be a string, got {type(npc_response['response'])}"


