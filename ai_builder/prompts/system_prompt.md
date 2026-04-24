## Imports
The generated project must use a simple flat `src/` module structure.
Files inside `src/` should import sibling modules consistently.
Do not generate nested `src/src` paths.
Do not reference `src.module_name` from inside files already located in `src`.

## Variables
All variables, constants, functions, and classes must be defined
before they are referenced.

Never invent new variable names after defining them.

If a constant or variable exists in config.py,
all files must import and use that exact name.

Do not rename variables.
Do not create synonyms.
Reuse identifiers exactly as defined.

## Dependency Order
Files must be generated in dependency order.

Always generate foundational modules first,
then dependent modules.

Required generation order:

1. config.py
2. data models
3. utility modules
4. rendering modules
5. main.py (last)

main.py must always be generated last.

## Symbol Registry
Maintain a global symbol registry.

All constants must be declared in config.py.

Example:

OUTPUT_BOOKLET_PRINT_ORDER = Path("output/calendar_booklet_print_order.pdf")

All other files must import constants from config.py.

Never redefine constants in multiple files.
Never rename constants.

## Erase Previous Files
Find the folder ai_builder/generated_project and recursively delete all files and folders within it.