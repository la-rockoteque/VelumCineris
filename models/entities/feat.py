"""
Feat entity model for D&D 5e.

Provides type-safe validation for feat data from Google Sheets.
"""

import pandas as pd
from ..base import BaseEntity


class Feat(BaseEntity):
    """
    D&D 5e Feat model.

    Represents a character feat in 5etools JSON format.
    """

    @classmethod
    def from_row(cls, row: pd.Series, source: str, json_source: str) -> 'Feat':
        """
        Create Feat from DataFrame row.

        Args:
            row: DataFrame row from Google Sheets
            source: Source filter (e.g., "VSTGCC")
            json_source: JSON source identifier

        Returns:
            Validated Feat instance
        """
        # Collect entries starting with flavor text, then all columns after "Feat"
        entries = []

        # Add flavor text
        if pd.notnull(row.get("Flavor Text")):
            entries.append(row.get("Flavor Text"))

        # Add all columns after "Feat" column
        try:
            feat_pos = row.index.get_loc("Feat")
            feat_entries = row.iloc[feat_pos:].dropna().tolist()
            entries.extend(feat_entries)
        except (KeyError, AttributeError):
            # If "Feat" column doesn't exist, just use flavor text
            pass

        return cls(
            source=json_source,
            name=row.get("Name", "Unnamed Feat").lower(),
            entries=entries
        )
