import openai

# Replace with your OpenAI API key
openai.api_key = "YOUR_OPENAI_API_KEY"

def get_gpt_response(prompt: str) -> str:
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=100
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error while getting response from GPT: {e}"
