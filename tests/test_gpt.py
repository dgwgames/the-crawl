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
    prompt = "Greet the adventurer"

    # When
    response = client.post("/gpt_interaction", json={"prompt": prompt})
    logger.info(f"Real response: {response.json()}")

    # Update the expected response key to 'greeting'
    logger.info(response.json()['response']["greeting"])
    assert 'greeting' in response.json()['response'], "Expected 'greeting' in response"
