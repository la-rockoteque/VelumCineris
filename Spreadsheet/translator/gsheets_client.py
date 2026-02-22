"""
Compatibility wrapper for translator Google Sheets access.

Canonical implementation now lives in `Spreadsheet/sheets.py`.
"""

from pathlib import Path
import sys

try:
    from Spreadsheet.sheets import (
        OfflineTranslatorSheetsClient as OfflineSheetsClient,
        TabKey,
        TranslatorSheetsClient as GSheetsClient,
        gsheets,
    )
except ModuleNotFoundError:
    # Allow running from inside the Spreadsheet/translator directory.
    sys.path.append(str(Path(__file__).resolve().parents[2]))
    from Spreadsheet.sheets import (  # type: ignore[no-redef]
        OfflineTranslatorSheetsClient as OfflineSheetsClient,
        TabKey,
        TranslatorSheetsClient as GSheetsClient,
        gsheets,
    )

__all__ = [
    "GSheetsClient",
    "OfflineSheetsClient",
    "TabKey",
    "gsheets",
]
