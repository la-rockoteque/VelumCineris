from __future__ import annotations

from typing import Any

import inflection
import pandas as pd


def map_language_row(row: Any, *, json_source: str) -> dict[str, Any]:
    return {
        "name": row.get("Name"),
        "source": json_source,
        "type": row.get("Type").lower(),
        **(
            {
                "typicalSpeakers": [
                    (
                        f"{{@filter {inflection.pluralize(speaker)}|bestiary|type=humanoid|"
                        f"tag= any race;{speaker}}}"
                    )
                    for speaker in row.get("Races").split(", ")
                ]
            }
            if pd.notnull(row.get("Races"))
            else {}
        ),
        **(
            {"script": row.get("Script").lower()}
            if pd.notnull(row.get("Script"))
            else {}
        ),
        "page": 0,
        "entries": [
            row.get("Description"),
        ],
    }
