"""
Feat converter for transforming Google Sheets feat data to Pydantic models.
"""

from .base import BaseConverter
from models.entities.feat import Feat


class FeatConverter(BaseConverter[Feat]):
    """Converter for feat entities."""

    entity_class = Feat
    sheet_gid = "1076107525"
    name_column = "Name"

    def convert_row(self, row, source: str, json_source: str) -> Feat:
        return Feat.from_row(row, source=source, json_source=json_source)
