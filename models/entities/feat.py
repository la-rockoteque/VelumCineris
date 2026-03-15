"""
Feat entity model for D&D 5e.

Provides type-safe validation for feat data from Google Sheets.
"""

from ..base import BaseEntity
from ..row_access import iter_present_values, optional_text, row_value, values_after_key


class Feat(BaseEntity):
    """
    D&D 5e Feat model.

    Represents a character feat in 5etools JSON format.
    """

    @classmethod
    def from_row(cls, row, source: str, json_source: str) -> 'Feat':
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
        flavor_text = optional_text(row_value(row, "Flavor Text"))
        if flavor_text:
            entries.append(flavor_text)

        # Add all columns after "Feat" column
        try:
            feat_entries = iter_present_values(values_after_key(row, "Feat"))
            entries.extend(feat_entries)
        except (KeyError, AttributeError, TypeError):
            # If "Feat" column doesn't exist, just use flavor text
            pass

        return cls(
            source=json_source,
            name=(optional_text(row_value(row, "Name")) or "Unnamed Feat").lower(),
            entries=entries
        )
