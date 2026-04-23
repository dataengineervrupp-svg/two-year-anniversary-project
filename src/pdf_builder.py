from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List

from reportlab.lib.colors import Color
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from calendar_data import DayCell, MonthData, PageData


PAGE_WIDTH, PAGE_HEIGHT = letter

# Page margins
MARGIN_X = 42
MARGIN_Y = 42
COLUMN_GAP = 32

CONTENT_WIDTH = PAGE_WIDTH - (2 * MARGIN_X)
CONTENT_HEIGHT = PAGE_HEIGHT - (2 * MARGIN_Y)
COLUMN_WIDTH = (CONTENT_WIDTH - COLUMN_GAP) / 2

TEXT_DARK = Color(0.15, 0.15, 0.15)
TEXT_MID = Color(0.45, 0.45, 0.45)
TEXT_LIGHT = Color(0.62, 0.62, 0.62)

LIGHT_GRID = Color(0.86, 0.86, 0.86)
LIGHTER_GRID = Color(0.93, 0.93, 0.93)
MONTH_MARK = Color(0.78, 0.78, 0.78)


@dataclass(frozen=True)
class ColumnWeek:
    month_name: str
    year: int
    week_index_in_month: int
    days: List[DayCell]
    starts_month: bool


def draw_weekday_header(
    c: canvas.Canvas,
    weekday_headers: List[str],
    x: float,
    y: float,
    width: float,
) -> None:
    col_width = width / 7

    c.setFillColor(TEXT_MID)
    c.setFont("Helvetica", 7)

    for i, header in enumerate(weekday_headers):
        header_x = x + i * col_width + col_width / 2
        c.drawCentredString(header_x, y, header)


def build_column_weeks(months: List[MonthData]) -> List[ColumnWeek]:
    """
    Flatten multiple months into one continuous stream of weeks.
    Weeks that contain no current-month dates are omitted.
    """
    result: List[ColumnWeek] = []

    for month in months:
        for week_idx, week in enumerate(month.weeks):
            current_month_days = [day for day in week if day.in_current_month]
            if not current_month_days:
                continue

            result.append(
                ColumnWeek(
                    month_name=month.month_name,
                    year=month.year,
                    week_index_in_month=week_idx,
                    days=week,
                    starts_month=(week_idx == 0),
                )
            )

    return result


def draw_continuous_column(
    c: canvas.Canvas,
    months: List[MonthData],
    x: float,
    y_bottom: float,
    width: float,
    height: float,
) -> None:
    """
    Draw one continuous column covering three months.
    The weekly rows flow continuously across month boundaries.
    """
    weekday_height = 12
    top_padding = 6
    bottom_padding = 8
    side_padding = 4
    month_label_gap = 10

    weekday_y = y_bottom + height - 10

    # Weekday header (once)
    draw_weekday_header(c, months[0].weekday_headers, x, weekday_y, width)

    weeks = build_column_weeks(months)

    month_start_count = sum(1 for w in weeks if w.starts_month)
    label_space_total = month_start_count * month_label_gap

    grid_top = weekday_y - weekday_height - top_padding
    grid_bottom = y_bottom + bottom_padding

    grid_left = x + side_padding
    grid_right = x + width - side_padding
    grid_width = grid_right - grid_left
    available_grid_height = grid_top - grid_bottom - label_space_total

    num_rows = len(weeks)
    col_width = grid_width / 7
    row_height = available_grid_height / num_rows if num_rows else 0

    current_y_top = grid_top

    for row_idx, week in enumerate(weeks):
        if week.starts_month:
            c.setFillColor(TEXT_LIGHT)
            c.setFont("Helvetica-Bold", 8)
            c.drawString(grid_left, current_y_top - 7, f"{week.month_name} {week.year}")
            current_y_top -= month_label_gap

        row_top = current_y_top
        row_bottom = row_top - row_height

        # Horizontal guides
        c.setStrokeColor(LIGHT_GRID)
        c.setLineWidth(0.3)
        c.line(grid_left, row_top, grid_right, row_top)
        if row_idx == len(weeks) - 1:
            c.line(grid_left, row_bottom, grid_right, row_bottom)

        # Slight emphasis at month starts
        if week.starts_month:
            c.setStrokeColor(MONTH_MARK)
            c.setLineWidth(0.45)
            c.line(grid_left, row_top, grid_right, row_top)

        # Vertical guides
        c.setStrokeColor(LIGHTER_GRID)
        c.setLineWidth(0.2)
        for col in range(8):
            line_x = grid_left + col * col_width
            c.line(line_x, row_top, line_x, row_bottom)

        # Day numbers
        for col_idx, day in enumerate(week.days):
            if not day.in_current_month:
                continue

            text_x = grid_left + col_idx * col_width + 3
            text_y = row_top - 9

            c.setFillColor(TEXT_DARK)
            c.setFont("Helvetica", 7.5)

            label = str(day.day)
            if day.is_special and day.special_emoji:
                label = f"{day.day} {day.special_emoji}"
            elif day.is_special and day.special_label:
                label = f"{day.day} *"

            c.drawString(text_x, text_y, label)

        current_y_top = row_bottom


def draw_page_of_months(
    c: canvas.Canvas,
    page_data: PageData,
) -> None:
    left_months = page_data.months[:3]
    right_months = page_data.months[3:6]

    left_x = MARGIN_X
    right_x = MARGIN_X + COLUMN_WIDTH + COLUMN_GAP
    y_bottom = MARGIN_Y
    column_height = CONTENT_HEIGHT

    if left_months:
        draw_continuous_column(
            c=c,
            months=left_months,
            x=left_x,
            y_bottom=y_bottom,
            width=COLUMN_WIDTH,
            height=column_height,
        )

    if right_months:
        draw_continuous_column(
            c=c,
            months=right_months,
            x=right_x,
            y_bottom=y_bottom,
            width=COLUMN_WIDTH,
            height=column_height,
        )


def build_proof_pdf(
    output_path: str | Path,
    page_data: PageData,
) -> Path:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    c = canvas.Canvas(str(output_path), pagesize=letter)
    draw_page_of_months(c, page_data)
    c.showPage()
    c.save()

    return output_path