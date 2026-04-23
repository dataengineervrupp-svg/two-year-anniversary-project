from __future__ import annotations

import calendar
from dataclasses import dataclass, field
from datetime import date
from typing import Dict, List, Optional


@dataclass(frozen=True)
class SpecialDate:
    """Represents a special annotated date in the calendar."""
    dt: date
    label: str
    emoji: str = ""


@dataclass(frozen=True)
class DayCell:
    """Represents a single cell in a month grid."""
    dt: date
    day: int
    in_current_month: bool
    special_label: str = ""
    special_emoji: str = ""

    @property
    def is_special(self) -> bool:
        return bool(self.special_label or self.special_emoji)


@dataclass(frozen=True)
class MonthData:
    """Represents all display data needed for one month."""
    year: int
    month: int
    month_name: str
    weekday_headers: List[str]
    weeks: List[List[DayCell]]


@dataclass(frozen=True)
class PageData:
    """Represents one printable page containing multiple months."""
    page_number: int
    months: List[MonthData] = field(default_factory=list)


def iter_months(start_year: int, start_month: int, end_year: int, end_month: int):
    """
    Yield (year, month) pairs inclusive from start to end.
    """
    year, month = start_year, start_month

    while (year, month) <= (end_year, end_month):
        yield year, month
        if month == 12:
            year += 1
            month = 1
        else:
            month += 1


def build_special_dates_lookup(special_dates: Optional[List[SpecialDate]] = None) -> Dict[date, SpecialDate]:
    """
    Convert a list of SpecialDate objects into a date-keyed lookup dictionary.
    """
    if not special_dates:
        return {}
    return {item.dt: item for item in special_dates}


def build_month_data(
    year: int,
    month: int,
    special_lookup: Optional[Dict[date, SpecialDate]] = None,
    week_starts_on_sunday: bool = True,
) -> MonthData:
    """
    Build all display data for a single month, including leading/trailing days.
    """
    if special_lookup is None:
        special_lookup = {}

    first_weekday = calendar.SUNDAY if week_starts_on_sunday else calendar.MONDAY
    cal = calendar.Calendar(firstweekday=first_weekday)

    weekday_headers = (
        ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        if week_starts_on_sunday
        else ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    )

    weeks: List[List[DayCell]] = []

    for week in cal.monthdatescalendar(year, month):
        week_cells: List[DayCell] = []
        for dt in week:
            special = special_lookup.get(dt)
            week_cells.append(
                DayCell(
                    dt=dt,
                    day=dt.day,
                    in_current_month=(dt.month == month),
                    special_label=special.label if special else "",
                    special_emoji=special.emoji if special else "",
                )
            )
        weeks.append(week_cells)

    return MonthData(
        year=year,
        month=month,
        month_name=calendar.month_name[month],
        weekday_headers=weekday_headers,
        weeks=weeks,
    )


def build_calendar_range(
    start_year: int,
    start_month: int,
    end_year: int,
    end_month: int,
    special_dates: Optional[List[SpecialDate]] = None,
    week_starts_on_sunday: bool = True,
) -> List[MonthData]:
    """
    Build MonthData objects for an inclusive range of months.
    """
    special_lookup = build_special_dates_lookup(special_dates)

    months: List[MonthData] = []
    for year, month in iter_months(start_year, start_month, end_year, end_month):
        months.append(
            build_month_data(
                year=year,
                month=month,
                special_lookup=special_lookup,
                week_starts_on_sunday=week_starts_on_sunday,
            )
        )
    return months


def chunk_months_into_pages(months: List[MonthData], months_per_page: int = 4) -> List[PageData]:
    """
    Group months into printable pages.
    """
    pages: List[PageData] = []

    for i in range(0, len(months), months_per_page):
        chunk = months[i:i + months_per_page]
        pages.append(
            PageData(
                page_number=(i // months_per_page) + 1,
                months=chunk,
            )
        )

    return pages


def default_special_dates() -> List[SpecialDate]:
    """
    Placeholder special dates for early development.
    Replace or expand these as the gift details become more specific.
    """
    return [
        SpecialDate(dt=date(2025, 4, 29), label="Anniversary", emoji="❤️"),
        SpecialDate(dt=date(2026, 4, 29), label="Anniversary", emoji="❤️"),
    ]


def build_project_calendar_data() -> List[PageData]:
    """
    Build the inside calendar pages for the project:
    May 2024 through April 2026, 6 months per page.
    """
    months = build_calendar_range(
        start_year=2024,
        start_month=5,
        end_year=2026,
        end_month=4,
        special_dates=default_special_dates(),
        week_starts_on_sunday=True,
    )

    return chunk_months_into_pages(months, months_per_page=6)


if __name__ == "__main__":
    pages = build_project_calendar_data()

    print(f"Total pages: {len(pages)}")
    for page in pages:
        labels = [f"{m.month_name} {m.year}" for m in page.months]
        print(f"Page {page.page_number}: {', '.join(labels)}")