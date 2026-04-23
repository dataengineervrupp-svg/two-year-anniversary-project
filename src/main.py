from __future__ import annotations

from pathlib import Path

from calendar_data import build_project_calendar_data
from pdf_builder import (
    build_combined_pdf,
    build_cover_pdf,
    build_full_pdf,
    build_imposed_booklet_pdf,
)


def main() -> None:
    pages = build_project_calendar_data()

    inside_pdf_path = build_full_pdf(
        Path("output") / "calendar_inside_pages.pdf",
        pages,
    )

    cover_pdf_path = build_cover_pdf(
        Path("output") / "calendar_cover_page.pdf",
    )

    combined_pdf_path = build_combined_pdf(
        Path("output") / "calendar_complete.pdf",
        pages,
    )

    booklet_pdf_path = build_imposed_booklet_pdf(
        Path("output") / "calendar_booklet_print_order.pdf",
        pages,
    )

    print(f"Created inside pages PDF: {inside_pdf_path.resolve()}")
    print(f"Created cover page PDF: {cover_pdf_path.resolve()}")
    print(f"Created combined PDF: {combined_pdf_path.resolve()}")
    print(f"Created booklet print-order PDF: {booklet_pdf_path.resolve()}")
    print(f"Inside calendar pages: {len(pages)}")
    print("Booklet print-order pages: 8")


if __name__ == "__main__":
    main()