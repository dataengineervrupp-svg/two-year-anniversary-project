from __future__ import annotations

import os

from dotenv import load_dotenv
from openai import OpenAI


def main() -> None:
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY was not found. Check your .env file.")

    client = OpenAI(api_key=api_key)

    response = client.responses.create(
        model="gpt-5.4",
        input="Reply with exactly: API smoke test passed",
    )

    print(response.output_text)


if __name__ == "__main__":
    main()