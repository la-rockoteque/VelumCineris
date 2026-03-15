from __future__ import annotations

from Spreadsheet.sheets import ContentSheetsClient, ContentType

SUPPORTED_CONTENT_TYPES: tuple[ContentType, ...] = ("fantasy", "modern")


def normalize_content_type(content_type: str) -> ContentType:
    normalized = str(content_type).strip().lower()
    if normalized not in SUPPORTED_CONTENT_TYPES:
        raise ValueError(
            f"Unknown content type '{content_type}'. Expected one of: {sorted(SUPPORTED_CONTENT_TYPES)}"
        )
    return normalized


def get_content_client(content_type: str) -> ContentSheetsClient:
    normalized: ContentType = normalize_content_type(content_type)
    return ContentSheetsClient(normalized)


def list_named_sheets(content_type: str) -> tuple[str, ...]:
    normalized: ContentType = normalize_content_type(content_type)
    return tuple(ContentSheetsClient.SHEET_GIDS[normalized].keys())


def default_spreadsheet_id(content_type: str = "fantasy") -> str:
    normalized: ContentType = normalize_content_type(content_type)
    return ContentSheetsClient.SPREADSHEETS[normalized]
