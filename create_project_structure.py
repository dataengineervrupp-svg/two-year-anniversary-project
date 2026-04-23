"""
create_project_structure.py

Creates the folder structure and starter spec files for the
calendar PDF project.

Safe to re-run: existing files will not be overwritten.
"""

from pathlib import Path

# ---------------------------------------------------------
# Project Root Name
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).parent

# ---------------------------------------------------------
# Directory Structure
# ---------------------------------------------------------

DIRECTORIES = [
    "specs",
    "prompts",
    "src",
    "output",
    "tests",
    "tools",
]

# ---------------------------------------------------------
# Spec Files (with starter content)
# ---------------------------------------------------------

SPEC_FILES = {
    "specs/project_overview.md": """# Project Overview

## Purpose

Generate a printable PDF calendar covering the last two years.

## High-Level Goals

- Generate a 24-month printable calendar
- One month per page
- Designed for clean printing
- Fully driven by text specifications
- Allow ChatGPT-assisted file generation and modification

## Version

v0.1 — Initial scaffolding
""",

    "specs/pdf_requirements.md": """# PDF Requirements

## Page Setup

Paper Size: (TBD)
Orientation: (TBD)
Margins: (TBD)

## Calendar Scope

Number of Months: 24
Date Range: Last two full years

## Visual Style

Color Mode: Black and White
Font: (TBD)
Weekend Styling: (TBD)

## Output Location

output/calendar_last_two_years.pdf
""",

    "specs/layout_rules.md": """# Layout Rules

## Month Page Layout

- Month title at top
- Weekday headers below title
- Date grid beneath weekday headers

## Grid Behavior

- Weeks begin on Monday or Sunday (TBD)
- Include leading/trailing days (TBD)

## Notes Section

(TBD — optional notes area under calendar)
""",

    "specs/change_log.md": """# Change Log

## v0.1

Initial project structure created.
""",

    "specs/task_queue.md": """# Task Queue

## Current Tasks

1. Create Python virtual environment
2. Install required libraries
3. Generate date logic for last 24 months
4. Render first test month PDF

## Future Tasks

- Build full PDF generator
- Add layout customization
- Add ChatGPT file automation
""",
}

# ---------------------------------------------------------
# Prompt Files
# ---------------------------------------------------------

PROMPT_FILES = {
    "prompts/file_generation_prompt.md": """# File Generation Prompt

Use this template when creating new files.

## Instructions

Generate a complete Python file based on the specifications.

Requirements:

- Follow layout rules
- Use existing project structure
- Include docstrings
- Include type hints where possible
""",

    "prompts/file_update_prompt.md": """# File Update Prompt

Use this template when modifying files.

## Instructions

Update the file based on spec changes.

Requirements:

- Preserve existing structure
- Update only required sections
- Maintain readability
""",
}

# ---------------------------------------------------------
# Source Files (empty placeholders)
# ---------------------------------------------------------

SOURCE_FILES = [
    "src/main.py",
    "src/calendar_data.py",
    "src/pdf_builder.py",
    "src/layout.py",
    "src/config.py",
]

# ---------------------------------------------------------
# Test Files
# ---------------------------------------------------------

TEST_FILES = [
    "tests/test_dates.py",
    "tests/test_layout.py",
]

# ---------------------------------------------------------
# Tool Files
# ---------------------------------------------------------

TOOL_FILES = [
    "tools/apply_generated_patch.py",
]

# ---------------------------------------------------------
# Other Files
# ---------------------------------------------------------

ROOT_FILES = {
    "README.md": """# Calendar PDF Project

This project generates a printable PDF calendar covering
the last two years.

The system is driven by text specifications located in:

specs/

ChatGPT will be used to generate and update files
based on these specifications.
""",

    "requirements.txt": """reportlab
""",
}


# ---------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------

def create_directory(path: Path):
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {path}")
    else:
        print(f"Directory exists: {path}")


def create_file(path: Path, content: str = ""):
    if not path.exists():
        path.write_text(content)
        print(f"Created file: {path}")
    else:
        print(f"File exists: {path}")


# ---------------------------------------------------------
# Main Execution
# ---------------------------------------------------------

def main():

    print("\nCreating project structure...\n")

    # Root directory
    create_directory(PROJECT_ROOT)

    # Create directories
    for directory in DIRECTORIES:
        create_directory(PROJECT_ROOT / directory)

    # Create spec files
    for file_path, content in SPEC_FILES.items():
        create_file(PROJECT_ROOT / file_path, content)

    # Create prompt files
    for file_path, content in PROMPT_FILES.items():
        create_file(PROJECT_ROOT / file_path, content)

    # Create source files
    for file_path in SOURCE_FILES:
        create_file(PROJECT_ROOT / file_path)

    # Create test files
    for file_path in TEST_FILES:
        create_file(PROJECT_ROOT / file_path)

    # Create tool files
    for file_path in TOOL_FILES:
        create_file(PROJECT_ROOT / file_path)

    # Create root-level files
    for file_path, content in ROOT_FILES.items():
        create_file(PROJECT_ROOT / file_path, content)

    print("\nProject structure created successfully.\n")


# ---------------------------------------------------------

if __name__ == "__main__":
    main()