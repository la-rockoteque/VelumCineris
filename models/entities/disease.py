"""
Disease entity model for D&D 5e.

Provides type-safe validation for disease data from Google Sheets.
"""

import pandas as pd
from ..base import BaseEntity


class Disease(BaseEntity):
    """
    D&D 5e Disease model.

    Represents a disease/illness in 5etools JSON format.
    """

    @classmethod
    def from_row(cls, row: pd.Series, source: str, json_source: str) -> 'Disease':
        """
        Create Disease from DataFrame row.

        Args:
            row: DataFrame row from Google Sheets
            source: Source filter (e.g., "ORIO")
            json_source: JSON source identifier (e.g., "GuideToOrimond")

        Returns:
            Validated Disease instance
        """
        # Collect entries (symptoms, effects, cure, prognosis)
        entries = []
        for field in ["Symptoms", "In-Game Effects", "Cure", "Prognosis"]:
            if pd.notnull(row.get(field)):
                entries.append(row.get(field))

        return cls(
            source=json_source,
            name=row.get("Name", "Unnamed Disease"),
            page=0,
            entries=entries
        )
