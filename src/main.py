from __future__ import annotations

from pathlib import Path

from calendar_data import build_project_calendar_data
from pdf_builder import build_combined_pdf, build_cover_pdf, build_full_pdf


def main() -> None:
    pages = build_project_calendar_data()

    inside_output_path = Path("output") / "calendar_inside_pages.pdf"
    inside_pdf_path = build_full_pdf(inside_output_path, pages)

    cover_output_path = Path("output") / "calendar_cover_page.pdf"
    cover_pdf_path = build_cover_pdf(cover_output_path)

    combined_output_path = Path("output") / "calendar_complete.pdf"
    combined_pdf_path = build_combined_pdf(combined_output_path, pages)

    print(f"Created inside pages PDF: {inside_pdf_path.resolve()}")
    print(f"Created cover page PDF: {cover_pdf_path.resolve()}")
    print(f"Created combined PDF: {combined_pdf_path.resolve()}")
    print(f"Total inside pages generated: {len(pages)}")
    print(f"Total pages in combined PDF: {len(pages) + 1}")


if __name__ == "__main__":
    main()