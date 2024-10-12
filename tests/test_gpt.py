from unittest.mock import patch
from app.core.gpt_service import get_gpt_response


@patch("app.core.gpt_service.openai.Completion.create")
def test_gpt_response(mock_openai):
    # Setup mock response
    mock_openai.return_value = type('obj', (object,), {
        'choices': [type('obj', (object,), {'text': "Hello, brave adventurer!"})]
    })()

    result = get_gpt_response("Greet the adventurer")
    assert result == "Hello, brave adventurer!"
