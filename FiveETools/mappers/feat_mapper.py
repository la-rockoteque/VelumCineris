from __future__ import annotations

from typing import Any


def map_feat_row(row: Any, *, json_source: str) -> dict[str, Any]:
    feat_pos = row.index.get_loc("Feat")
    return {
        "name": row.get("Name").lower(),
        "source": json_source,
        "entries": [
            row.get("Flavor Text"),
            *row.iloc[feat_pos:].dropna().tolist(),
        ],
    }
