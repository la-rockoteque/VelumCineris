"""
Background converter for transforming Google Sheets background data to Pydantic models.
"""

from .base import BaseConverter
from models.entities.background import Background


class BackgroundConverter(BaseConverter[Background]):
    """Converter for background entities."""

    entity_class = Background
    sheet_gid = "1186398440"
    name_column = "Background"

    def convert_row(self, row, source: str, json_source: str) -> Background:
        return Background.from_row(row, source=source, json_source=json_source)
