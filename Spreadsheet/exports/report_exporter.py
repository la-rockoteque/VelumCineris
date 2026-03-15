from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def build_default_report_path(report_name: str = "workbook_summary") -> Path:
    return Path("Spreadsheet/out") / f"{report_name}.json"


def write_json_report(
    payload: dict[str, Any],
    *,
    output_path: str | Path | None = None,
    report_name: str = "workbook_summary",
) -> Path:
    destination = (
        Path(output_path)
        if output_path is not None
        else build_default_report_path(report_name=report_name)
    )
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(payload, indent=2, ensure_ascii=True),
        encoding="utf-8",
    )
    return destination

