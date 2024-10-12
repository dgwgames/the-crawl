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
    logger.info(response.json()['response']["message"])

    # Then
    logger.info("Asserting the GPT interaction response is correct.")
    assert response.status_code == 200