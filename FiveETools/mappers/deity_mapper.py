from __future__ import annotations

from typing import Any

import pandas as pd


def _split_list(value: Any) -> list[str]:
    if pd.isnull(value):
        return []
    return [item.strip() for item in str(value).split(",") if item.strip()]


def map_fantasy_deity_row(row: Any, *, json_source: str) -> dict[str, Any]:
    return {
        "name": row.get("Name"),
        "source": json_source,
        "epithet": row.get("Epithet"),
        "pantheon": row.get("Pantheon"),
        "image": row.get("Image"),
        "domains": _split_list(row.get("Domains")),
        "plane": row.get("Plane"),
        "vstg": row.get("VSTG"),
        "alignment": row.get("Alignment"),
        "followers": row.get("Followers"),
        "symbol": row.get("Symbol"),
        "slogan": row.get("Slogan"),
        "link": row.get("Link"),
        "description": row.get("Description"),
        "lore": row.get("Lore"),
        "quote": row.get("Quote"),
    }


def map_modern_deity_row(row: Any, *, json_source: str) -> dict[str, Any]:
    return {
        "name": row.get("Name"),
        "source": json_source,
        "pantheon": "None",
        "symbol": row.get("Symbol") if pd.notnull(row.get("Symbol")) else "",
        "entries": [
            row.get("Description") if pd.notnull(row.get("Description")) else "",
        ],
        "page": 0,
        "alignment": [row.get("Alignment")[:1].upper()],
        **(
            {"altNames": row.get("Epithet").split(", ")}
            if pd.notnull(row.get("Epithet"))
            else {}
        ),
        "customProperties": {
            "Plane": row.get("Plane") if pd.notnull(row.get("Plane")) else "",
            "Followers": row.get("Followers") if pd.notnull(row.get("Followers")) else "",
            "Slogan": row.get("Slogan") if pd.notnull(row.get("Slogan")) else "",
            "Lore": row.get("Lore") if pd.notnull(row.get("Lore")) else "",
            "Quote": row.get("Quote") if pd.notnull(row.get("Quote")) else "",
        },
    }
