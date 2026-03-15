from __future__ import annotations

from typing import Any


def map_condition_row(row: Any, *, json_source: str) -> dict[str, Any]:
    return {
        "name": row.get("Condition Name"),
        "source": json_source,
        "entries": [
            *row.get("Condition Text").split(";"),
        ],
    }
