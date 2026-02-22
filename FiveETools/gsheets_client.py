"""
Compatibility wrapper for the shared Sheets client.

Canonical implementation now lives in `Spreadsheet/sheets.py`.
"""

from pathlib import Path
import sys

try:
    from Spreadsheet.sheets import (
        ContentSheetsClient,
        ContentType,
        fantasy_sheets,
        modern_sheets,
    )
except ModuleNotFoundError:
    # Allow running from inside the FiveETools directory.
    sys.path.append(str(Path(__file__).resolve().parents[1]))
    from Spreadsheet.sheets import (  # type: ignore[no-redef]
        ContentSheetsClient,
        ContentType,
        fantasy_sheets,
        modern_sheets,
    )

__all__ = [
    "ContentSheetsClient",
    "ContentType",
    "fantasy_sheets",
    "modern_sheets",
]
