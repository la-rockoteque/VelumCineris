"""
Condition converter for transforming Google Sheets condition data to Pydantic models.
"""

from .base import BaseConverter
from models.entities.condition import Condition


class ConditionConverter(BaseConverter[Condition]):
    """Converter for condition entities."""

    entity_class = Condition
    sheet_gid = "1321788284"
    name_column = "Condition Name"

    def convert_row(self, row, source: str, json_source: str) -> Condition:
        return Condition.from_row(row, source=source, json_source=json_source)
