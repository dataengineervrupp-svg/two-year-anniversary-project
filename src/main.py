from __future__ import annotations

from pathlib import Path

from calendar_data import build_project_calendar_data
from pdf_builder import build_proof_pdf


def main() -> None:
    pages = build_project_calendar_data()

    first_page = pages[0]

    output_path = Path("output") / "calendar_proof_page_1_six_months.pdf"
    pdf_path = build_proof_pdf(output_path, first_page)

    print(f"Created proof PDF: {pdf_path.resolve()}")


if __name__ == "__main__":
    main()