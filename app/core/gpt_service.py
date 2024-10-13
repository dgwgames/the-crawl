import json

import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def get_gpt_response(prompt: str, api_key: str = None, model: str = None):
    """Helper function to get a response from GPT using the updated client."""
    from openai import OpenAI
    try:
        # Use environment variable if API key is not provided
        if api_key is None:
            api_key = os.getenv("OPENAI_API_KEY")

        if model is None:
            model = os.getenv("AI_MODEL")

        # Set up the OpenAI client with the provided API key
        client = OpenAI()
        client.api_key = api_key

        # Prepare and send the request to OpenAI
        completion = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": f"{prompt}: respond in json"}],
            stream=False,
            response_format={ "type": "json_object" }
        )

        response_content = completion.choices[0].message.content

        # Remove newlines from the response JSON
        response_content = response_content.replace("\n", "")
        return json.loads(response_content)
    except Exception as e:
        return f"Error while getting response from GPT: {str(e)}"



