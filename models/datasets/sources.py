from __future__ import annotations

from Spreadsheet.core.Helpers.sheets import fantasy_sheets

SOURCES_GID = "340852453"
DEFAULT_SOURCE = "ORIO"


def resolve_source_context(source_code: str = DEFAULT_SOURCE) -> tuple[str, str]:
    """Resolve source and json_source from the shared sources sheet."""
    df_source = fantasy_sheets.get_sheet(SOURCES_GID)
    source_row = df_source[df_source["Source"] == source_code].iloc[0]
    json_source = str(source_row["json"])
    return source_code, json_source


source, json_source = resolve_source_context()
