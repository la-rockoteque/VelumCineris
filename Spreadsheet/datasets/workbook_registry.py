from __future__ import annotations

from Spreadsheet.core.workbook_models.registry import load_orimond_registry
from Spreadsheet.datasets.content_registry import default_spreadsheet_id


def load_registry(
    *,
    source: str = "auto",
    xlsx_path: str = "Spreadsheet/Orimond.xlsx",
    spreadsheet_id: str | None = None,
    credentials_path: str | None = None,
):
    return load_orimond_registry(
        source=source,
        xlsx_path=xlsx_path,
        spreadsheet_id=spreadsheet_id or default_spreadsheet_id("fantasy"),
        credentials_path=credentials_path,
    )

