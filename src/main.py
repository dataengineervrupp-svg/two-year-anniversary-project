from __future__ import annotations

from pathlib import Path

from calendar_data import build_project_calendar_data
from pdf_builder import build_full_pdf


def main() -> None:
    pages = build_project_calendar_data()

    output_path = Path("output") / "calendar_inside_pages.pdf"
    pdf_path = build_full_pdf(output_path, pages)

    print(f"Created full calendar PDF: {pdf_path.resolve()}")
    print(f"Total inside pages generated: {len(pages)}")


if __name__ == "__main__":
    main()