from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Dict, List
from collections import defaultdict

import pandas as pd
from pathlib import Path


def load_dating_log_dataframe() -> pd.DataFrame:
    """
    Load the dating log CSV into a pandas DataFrame.
    Expects:
        dating_log_connie.csv in project root
    Returns:
        pandas DataFrame with parsed dates
    """

    project_root = Path(__file__).resolve().parent.parent
    csv_path = project_root / "dating_log_connie.csv"
    if not csv_path.exists():
        raise FileNotFoundError(
            f"Could not find CSV file at: {csv_path}"
        )
    df = pd.read_csv(csv_path)
    df["date"] = pd.to_datetime(df["Date_Date"]).dt.date
    df.drop(columns=['Date', 'Description'], inplace=True)
    df.rename(columns={'Date_Date':'date_str'}, inplace=True)
    return df

@dataclass(frozen=True)
class DateAnnotation:
    dt: date
    category: str
    marker: str
    label: str = ""


EVENT_DATES = {
    "Date": [],
    "Casual Date": [],
    "Category 3": [],
    "The Barn": [],
    "The ~Barn~":[],
    "Trips": ["2024-10-28", "2024-10-29"],
    "Overnights": ["2025-07-03"],
    "Test": ["2024-05-10", "2024-06-15", "2024-08-01"],
}

CATEGORY_STYLES = {
    "Trips": {"marker": "T", "label": "Trip"},
    "Overnights": {"marker": "O", "label": "Overnight"},
    "Test": {"marker": "X", "label": "Test"},
}


def parse_iso_date(value: str) -> date:
    return date.fromisoformat(value)


def build_annotations() -> List[DateAnnotation]:
    annotations: List[DateAnnotation] = []

    for category, date_strings in EVENT_DATES.items():
        style = CATEGORY_STYLES.get(category)
        if style is None:
            raise ValueError(f"Missing CATEGORY_STYLES entry for category: {category}")

        for value in date_strings:
            annotations.append(
                DateAnnotation(
                    dt=parse_iso_date(value),
                    category=category,
                    marker=style["marker"],
                    label=style.get("label", ""),
                )
            )

    return annotations


def build_annotation_lookup() -> Dict[date, List[DateAnnotation]]:
    lookup: Dict[date, List[DateAnnotation]] = defaultdict(list)

    for annotation in build_annotations():
        lookup[annotation.dt].append(annotation)

    return dict(lookup)

if __name__ == "__main__":
    df = load_dating_log_dataframe()
    print(df.head())
    print(df.dtypes)
    # print(df[df['Category'] == 'Category 3'].head())
    print(df['Category'].value_counts())