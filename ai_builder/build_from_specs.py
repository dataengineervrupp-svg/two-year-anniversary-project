from __future__ import annotations

import json
import re
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
import shutil

from ast_helper import is_constant_name, extract_python_symbols

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SPECS_DIR = PROJECT_ROOT / "specs"
OUTPUT_DIR = PROJECT_ROOT / "ai_builder" / "generated_project"
if OUTPUT_DIR.exists():
    shutil.rmtree(OUTPUT_DIR)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

MODEL = "gpt-5.4-mini"

def read_specs() -> str:
    chunks = []

    for path in sorted(SPECS_DIR.glob("*.md")):
        chunks.append(f"\n\n# FILE: specs/{path.name}\n")
        chunks.append(path.read_text(encoding="utf-8"))

    return "".join(chunks)

PROMPTS_DIR = PROJECT_ROOT / "ai_builder" / "prompts"

def read_prompt(filename: str) -> str:
    path = PROMPTS_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"Missing prompt file: {path}")
    return path.read_text(encoding="utf-8")

def get_client() -> OpenAI:
    load_dotenv()
    return OpenAI(api_key=os.environ["OPENAI_API_KEY"])

def extract_json(text: str) -> dict:
    """
    Extract JSON object from model response.
    """

    match = re.search(r"\{.*\}", text, re.DOTALL)

    if not match:
        raise ValueError("No JSON object found in response")

    json_text = match.group()

    return json.loads(json_text)

def load_manifest() -> dict:
    path = OUTPUT_DIR / "build_manifest.json"
    if not path.exists():
        return {"files": []}
    return json.loads(path.read_text(encoding="utf-8"))

def save_manifest(manifest: dict) -> None:
    path = OUTPUT_DIR / "build_manifest.json"
    path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

def update_manifest_for_file(file_item: dict) -> None:
    manifest = load_manifest()
    relative_path = file_item["path"]
    full_path = OUTPUT_DIR / relative_path
    entry = {
        "path": relative_path,
        "purpose": file_item.get("purpose", ""),
        "dependencies": file_item.get("dependencies", []),
        "generated": True,
    }
    if full_path.suffix == ".py":
        entry["symbols"] = extract_python_symbols(full_path)
    manifest.setdefault("files", [])
    # Replace existing entry if rerunning
    manifest["files"] = [
        item for item in manifest["files"]
        if item.get("path") != relative_path
    ]
    manifest["files"].append(entry)
    save_manifest(manifest)

def ask_for_file_plan(client: OpenAI, specs_text: str) -> list[dict]:
    system_prompt = read_prompt("system_prompt.md")
    file_plan_prompt = read_prompt("file_plan_prompt.md")
    prompt = f"""
    {file_plan_prompt}

    Project specifications:

    {specs_text}

    Your task:
    Create a complete file plan.
    Return ONLY valid JSON.
    The JSON must be:
    {{
    "files": [
        {{
        "path": "relative/file/path.py",
        "purpose": "short description",
        "dependencies": ["file1.py"]
        }}
    ]
    }}

    Rules:
    - Return JSON only
    - No commentary
    - No explanations
    - No markdown fences
    - No extra text before or after JSON
    - config.py must appear first
    - main.py must appear last
    - Files must be listed in dependency order
    """
    response = client.responses.create(
        model=MODEL,
        input=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )
    plan_obj = extract_json(response.output_text)
    file_plan = plan_obj["files"]
    return file_plan

def generate_file(client: OpenAI, specs_text: str, file_plan: list[dict], file_item: dict) -> str:
    # config_path = OUTPUT_DIR / "src" / "config.py"
    # if file_item["path"] != "src/config.py" and not config_path.exists():
    #     raise RuntimeError(
    #         "config.py must be generated before other files."
    #     )
    # if config_path.exists():
    #     config_text = config_path.read_text(encoding='utf-8')
    # else:
    #     config_text = None
    # if config_text:
    #     config_block = f"""
    #     Existing config.py:
    #     {config_text}
    #     All constants must be reused exactly.
    #     Do not rename constants.
    #     Do not create duplicates.

    #     """
    # else:
    #     config_block = ""
    manifest = load_manifest()
    manifest_text = json.dumps(manifest, indent=2)
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

Current generated project manifest:

{manifest_text}

Rules:

- You may only import project symbols that appear in this manifest.
- Do not invent classes, functions, constants, or dataclass fields.
- If a project dependency has not been generated yet, do not import from it.
- Reuse symbol names exactly as shown.

The csv file for annotations is dating_log_connie.csv in the parent of the parent of the root folder. Use columns Date and Category.

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
    file_plan.sort(
        key=lambda f: (
            f["path"] != "src/config.py",
            f["path"] == "src/main.py",
        )
    )

    plan_path = OUTPUT_DIR / "file_plan.json"
    plan_path.write_text(json.dumps(file_plan, indent=2), encoding="utf-8")

    for file_item in file_plan:
        content = generate_file(client, specs_text, file_plan, file_item)
        manifest = load_manifest()
        write_file(file_item["path"], content)
        update_manifest_for_file(file_item)
        compile(content, file_item["path"], "exec")


if __name__ == "__main__":
    main()