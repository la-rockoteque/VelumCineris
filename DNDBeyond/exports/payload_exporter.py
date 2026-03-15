from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def build_default_output_path(*, entity_type: str, setting: str) -> Path:
    return Path("DNDBeyond/out") / f"{entity_type}_payloads_{setting}.json"


def write_payloads(
    payloads: list[dict[str, Any]],
    *,
    output_path: str | Path | None = None,
    entity_type: str,
    setting: str,
) -> Path:
    destination = (
        Path(output_path)
        if output_path is not None
        else build_default_output_path(entity_type=entity_type, setting=setting)
    )
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(payloads, indent=2, ensure_ascii=True),
        encoding="utf-8",
    )
    return destination

