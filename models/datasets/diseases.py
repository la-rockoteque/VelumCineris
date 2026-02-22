from FiveETools.fantasy.sources import source, json_source
from FiveETools.gsheets_client import fantasy_sheets


# NEW: Pydantic-based conversion for type safety
from Spreadsheet.converters.disease import DiseaseConverter
from models.entities.disease import Disease
from typing import List

converter = DiseaseConverter(fantasy_sheets)
disease_pydantic: List[Disease] = converter.convert_all(
    source_filter=None,  # Diseases don't use source filter
    source=source,
    json_source=json_source
)
