"""
Condition entity model for D&D 5e.

Provides type-safe validation for condition data from Google Sheets.
"""

import pandas as pd
from ..base import BaseEntity


class Condition(BaseEntity):
    """
    D&D 5e Condition model.

    Represents a status condition in 5etools JSON format.
    """

    @classmethod
    def from_row(cls, row: pd.Series, source: str, json_source: str) -> 'Condition':
        """
        Create Condition from DataFrame row.

        Args:
            row: DataFrame row from Google Sheets
            source: Source filter (e.g., "VSTGCC")
            json_source: JSON source identifier

        Returns:
            Validated Condition instance
        """
        # Split condition text by semicolons
        entries = []
        if pd.notnull(row.get("Condition Text")):
            entries = [e.strip() for e in row.get("Condition Text").split(";") if e.strip()]

        return cls(
            source=json_source,
            name=row.get("Condition Name", "Unnamed Condition"),
            entries=entries
        )
