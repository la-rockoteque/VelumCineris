"""
Language converter for transforming Google Sheets language data to Pydantic models.
"""

from .base import BaseConverter
from models.entities.language import Language


class LanguageConverter(BaseConverter[Language]):
    """
    Converter for language entities.

    Transforms DataFrame rows to validated Language instances.
    """

    entity_class = Language
    sheet_gid = "163123529"  # Languages sheet GID
    name_column = "Name"

    def convert_row(self, row, source: str, json_source: str) -> Language:
        """
        Convert single language row.

        Args:
            row: DataFrame row with language data
            source: Source filter (e.g., "ORIO")
            json_source: JSON source identifier (e.g., "GuideToOrimond")

        Returns:
            Validated Language instance
        """
        return Language.from_row(row, source=source, json_source=json_source)
