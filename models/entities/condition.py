"""
Condition entity model for D&D 5e.

Provides type-safe validation for condition data from Google Sheets.
"""

from ..base import BaseEntity
from ..row_access import optional_text, row_value


class Condition(BaseEntity):
    """
    D&D 5e Condition model.

    Represents a status condition in 5etools JSON format.
    """

    @classmethod
    def from_row(cls, row, source: str, json_source: str) -> 'Condition':
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
        condition_text = optional_text(row_value(row, "Condition Text"))
        if condition_text:
            entries = [e.strip() for e in condition_text.split(";") if e.strip()]

        return cls(
            source=json_source,
            name=optional_text(row_value(row, "Condition Name")) or "Unnamed Condition",
            entries=entries
        )
