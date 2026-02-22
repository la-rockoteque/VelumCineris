"""
Magic Item converter for transforming Google Sheets magic item data to Pydantic models.
"""

from .base import BaseConverter
from models.entities.magic_item import MagicItem


class MagicItemConverter(BaseConverter[MagicItem]):
    """Converter for magic item entities."""

    entity_class = MagicItem
    sheet_gid = "695912920"
    name_column = "Name"

    def convert_row(self, row, source: str, json_source: str) -> MagicItem:
        return MagicItem.from_row(row, source=source, json_source=json_source)
