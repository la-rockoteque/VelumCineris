from __future__ import annotations

from Spreadsheet.sheets import ContentSheetsClient, fantasy_sheets, modern_sheets

SUPPORTED_SOURCES: tuple[str, ...] = ("fantasy", "modern")

_SHEETS_CLIENTS: dict[str, ContentSheetsClient] = {
    "fantasy": fantasy_sheets,
    "modern": modern_sheets,
}


def normalize_source(source: str) -> str:
    normalized = str(source).strip().lower()
    if normalized not in _SHEETS_CLIENTS:
        raise ValueError(
            f"Unknown source '{source}'. Expected one of: {sorted(SUPPORTED_SOURCES)}"
        )
    return normalized


def get_sheets_client(source: str) -> ContentSheetsClient:
    return _SHEETS_CLIENTS[normalize_source(source)]


def list_sources() -> tuple[str, ...]:
    return SUPPORTED_SOURCES

