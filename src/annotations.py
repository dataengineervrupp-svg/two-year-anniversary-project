from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Dict, List
from collections import defaultdict


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