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

df = load_dating_log_dataframe()

@dataclass(frozen=True)
class DateAnnotation:
    dt: date
    category: str
    marker: str
    label: str = ""


EVENT_DATES = {
    "Date": list(df[df['Category'] == 'Date']['date_str']),
    "Casual Date": list(df[df['Category'] == 'Casual Date']['date_str']),
    "Category 3": list(df[df['Category'] == 'Category 3']['date_str']),
    "Summer Blockbuster": ['2024-09-24', '2024-11-12', '2025-01-03', '2025-02-18', '2025-05-09', '2025-08-25', '2025-10-14', '2026-04-14'],
    "Wine Class":['2024-10-01', '2024-10-08', '2024-10-14', '2024-11-05', '2024-12-17', '2024-12-24', '2025-02-18', '2025-04-30', '2025-05-13', '2025-07-15', '2025-08-05', '2025-09-23', '2025-11-11', '2026-01-20'],
    "The Barn":['2024-05-07', '2024-08-09', '2024-12-06', '2026-02-13'],
    "Trip": list(df[df['Category'] == 'Trip']['date_str']),
    "Other": list(df[df['Category'] == 'Other']['date_str']),
}

CATEGORY_STYLES = {
    "Trip": {"marker": "T", "label": "Trip"},
    "Date": {"marker": "D", "label": "Date"},
    "Casual Date": {"marker": "C", "label":"Casual Date"},
    "Category 3": {"marker": "3", "label":"Category 3"},
    "Summer Blockbuster": {"marker": "a", "label": "Summer Blockbuster"},
    "Wine Class": {"marker": "p", "label": "Wine Class"},
    "The Barn": {"marker":"B", "label":"The Barn"},
    "Other": {"marker":"O", "label":"Other"}
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
    print(df.head())
    # print(df.dtypes)
    # print(df[df['Category'] == 'Category 3'].head())
    print(df['Category'].value_counts())
    print(list(df[df['Category'] == 'Trip']['date_str'])[0:5])