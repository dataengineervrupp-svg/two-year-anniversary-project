from __future__ import annotations

import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


PROJECT_ROOT = Path(__file__).resolve().parent.parent
SPECS_DIR = PROJECT_ROOT / "specs"
OUTPUT_DIR = PROJECT_ROOT / "ai_builder" / "generated_project"

MODEL = "gpt-5.4"


def read_specs() -> str:
    chunks = []

    for path in sorted(SPECS_DIR.glob("*.md")):
        chunks.append(f"\n\n# FILE: specs/{path.name}\n")
        chunks.append(path.read_text(encoding="utf-8"))

    return "".join(chunks)


def get_client() -> OpenAI:
    load_dotenv()
    return OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def ask_for_file_plan(client: OpenAI, specs_text: str) -> list[dict]:
    prompt = f"""
You are generating a local Python project from markdown specifications.

Return ONLY valid JSON.

The JSON must be a list of files to create.
Each item must have:
- path
- purpose
- dependencies

Do not include markdown fences.

Specifications:
{specs_text}
"""

    response = client.responses.create(
        model=MODEL,
        input=prompt,
    )

    return json.loads(response.output_text)


def generate_file(client: OpenAI, specs_text: str, file_plan: list[dict], file_item: dict) -> str:
    prompt = f"""
You are generating one file for a local Python project.

Return ONLY the full file content.
Do not include markdown fences.
Do not include explanations.

Project specifications:
{specs_text}

Full file plan:
{json.dumps(file_plan, indent=2)}

Generate this file:
{json.dumps(file_item, indent=2)}
"""

    response = client.responses.create(
        model=MODEL,
        input=prompt,
    )

    return response.output_text


def write_file(relative_path: str, content: str) -> None:
    path = OUTPUT_DIR / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"Wrote {path}")


def main() -> None:
    client = get_client()
    specs_text = read_specs()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    file_plan = ask_for_file_plan(client, specs_text)

    plan_path = OUTPUT_DIR / "file_plan.json"
    plan_path.write_text(json.dumps(file_plan, indent=2), encoding="utf-8")

    for file_item in file_plan:
        content = generate_file(client, specs_text, file_plan, file_item)
        write_file(file_item["path"], content)


if __name__ == "__main__":
    main()