import os

import requests
from dotenv import load_dotenv


# Load variables from .env
load_dotenv()


OPENROUTER_API_KEY = os.getenv(
    "OPENROUTER_API_KEY"
)

OPENROUTER_MODEL = os.getenv(
    "OPENROUTER_MODEL",
    "openai/gpt-4o-mini"
)

OPENROUTER_URL = (
    "https://openrouter.ai/api/v1/chat/completions"
)


def ask_llm(prompt):

    # --------------------------------------------------
    # Check API key
    # --------------------------------------------------

    if not OPENROUTER_API_KEY:

        raise ValueError(
            "OPENROUTER_API_KEY is not configured. "
            "Please add it to the .env file."
        )

    # --------------------------------------------------
    # Headers
    # --------------------------------------------------

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    # --------------------------------------------------
    # Request payload
    # --------------------------------------------------

    payload = {
        "model": OPENROUTER_MODEL,

        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],

        "temperature": 0
    }

    # --------------------------------------------------
    # Send request
    # --------------------------------------------------

    response = requests.post(
        OPENROUTER_URL,
        headers=headers,
        json=payload,
        timeout=60
    )

    # --------------------------------------------------
    # Handle API errors
    # --------------------------------------------------

    if response.status_code != 200:

        raise RuntimeError(
            f"OpenRouter API error "
            f"{response.status_code}: "
            f"{response.text}"
        )

    # --------------------------------------------------
    # Parse response
    # --------------------------------------------------

    data = response.json()

    try:

        return data["choices"][0]["message"]["content"]

    except (KeyError, IndexError):

        raise RuntimeError(
            f"Unexpected OpenRouter response: {data}"
        )