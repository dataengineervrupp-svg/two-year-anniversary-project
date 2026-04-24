Create a Python project that generates a printable calendar.

Required directory structure:

src/
    config.py
    calendar_data.py
    pdf_builder.py
    annotations.py
    main.py

requirements.txt

Each file must have a clear responsibility.

config.py:
    defines all constants
    defines output file paths

calendar_data.py:
    builds calendar date structures

annotations.py:
    loads CSV annotations

pdf_builder.py:
    renders PDF pages

main.py:
    orchestrates full PDF generation