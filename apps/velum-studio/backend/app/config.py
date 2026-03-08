from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[4]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from Spreadsheet.core.workbook_models.registry import ORIMOND_SPREADSHEET_ID  # noqa: E402


@dataclass(frozen=True)
class Settings:
    host: str = os.getenv("VELUM_HOST", "127.0.0.1")
    port: int = int(os.getenv("VELUM_PORT", "8765"))
    spreadsheet_id: str = os.getenv("VELUM_SPREADSHEET_ID", ORIMOND_SPREADSHEET_ID)
    xlsx_path: Path = Path(
        os.getenv("VELUM_XLSX_PATH", str(PROJECT_ROOT / "Spreadsheet/Orimond.xlsx"))
    )
    credentials_path: Path = Path(
        os.getenv("VELUM_GSHEETS_KEY_PATH", str(PROJECT_ROOT / "Spreadsheet/key.json"))
    )
    settings_path: Path = Path(
        os.getenv("VELUM_SETTINGS_PATH", str(Path.home() / ".velum"))
    )
    timeline_xlsx_path: Path = Path(
        os.getenv("VELUM_TIMELINE_XLSX_PATH", str(PROJECT_ROOT / "Timeline/Orimond Timeline.xlsx"))
    )
    timeline_spreadsheet_id: str = os.getenv("VELUM_TIMELINE_SPREADSHEET_ID", spreadsheet_id)
    assets_path: Path = Path(
        os.getenv("VELUM_ASSETS_PATH", str(PROJECT_ROOT / "assets"))
    )


settings = Settings()
