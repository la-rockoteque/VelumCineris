"""
Monster converter for transforming Google Sheets monster data to Pydantic models.
"""

from .base import BaseConverter
from models.entities.monster import Monster


class MonsterConverter(BaseConverter[Monster]):
    """
    Converter for monster/creature entities.

    Transforms DataFrame rows to validated Monster instances.
    """

    entity_class = Monster
    sheet_gid = "736393386"  # Monsters sheet GID
    name_column = "Name"  # Monsters use standard "Name" column

    def convert_row(self, row, source: str, json_source: str) -> Monster:
        """
        Convert single monster row.

        Args:
            row: DataFrame row with monster data
            source: Source filter (e.g., "ORIO")
            json_source: JSON source identifier (e.g., "GuideToOrimond")

        Returns:
            Validated Monster instance
        """
        return Monster.from_row(row, source=source, json_source=json_source)
