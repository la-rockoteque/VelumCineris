"""
Spell converter for transforming Google Sheets spell data to Pydantic models.
"""

from .base import BaseConverter
from models.entities.spell import Spell


class SpellConverter(BaseConverter[Spell]):
    """
    Converter for spell entities.

    Transforms DataFrame rows to validated Spell instances.
    """

    entity_class = Spell
    sheet_gid = "625265890"  # Spells sheet GID
    name_column = "Spell Name"  # Spells use "Spell Name" column

    def convert_row(self, row, source: str, json_source: str) -> Spell:
        """
        Convert single spell row.

        Args:
            row: DataFrame row with spell data
            source: Source filter (e.g., "ORIO")
            json_source: JSON source identifier (e.g., "ORIO")

        Returns:
            Validated Spell instance
        """
        return Spell.from_row(row, source=source, json_source=json_source)
