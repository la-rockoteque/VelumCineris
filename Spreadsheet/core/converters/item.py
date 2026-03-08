"""
Item converter for transforming Google Sheets item data to Pydantic models.
"""

from .base import BaseConverter
from models.entities.item import Item


class ItemConverter(BaseConverter[Item]):
    """Converter for item entities."""

    entity_class = Item
    sheet_gid = "876046336"
    name_column = "Name"

    def convert_row(self, row, source: str, json_source: str) -> Item:
        return Item.from_row(row, source=source, json_source=json_source)
