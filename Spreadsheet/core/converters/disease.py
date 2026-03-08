"""
Disease converter for transforming Google Sheets disease data to Pydantic models.
"""

from .base import BaseConverter
from models.entities.disease import Disease


class DiseaseConverter(BaseConverter[Disease]):
    """Converter for disease entities."""

    entity_class = Disease
    sheet_gid = "1196270347"
    name_column = "Name"

    def convert_row(self, row, source: str, json_source: str) -> Disease:
        return Disease.from_row(row, source=source, json_source=json_source)
