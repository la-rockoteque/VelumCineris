from __future__ import annotations

from typing import Any


def map_disease_row(row: Any, *, json_source: str) -> dict[str, Any]:
    return {
        "name": row.get("Name"),
        "source": json_source,
        "entries": [
            row.get("Symptoms"),
            row.get("In-Game Effects"),
            row.get("Cure"),
            row.get("Prognosis"),
        ],
        "page": 0,
    }
