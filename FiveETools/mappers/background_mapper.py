from __future__ import annotations

from typing import Any

import pandas as pd


def map_background_row(row: Any, *, source: str, json_source: str) -> dict[str, Any]:
    del source
    return {
        "name": row.get("Background"),
        "source": json_source,
        **(
            {
                "skillProficiencies": [
                    {skill.lower(): True for skill in row.get("Skills").split(", ")}
                ]
            }
            if pd.notnull(row.get("Skills")) and row.get("Skills")
            else {}
        ),
        "entries": [
            {
                "type": "list",
                "style": "list-hang-notitle",
                "items": [
                    *(
                        [
                            {
                                "type": "item",
                                "name": "Skill Proficiencies",
                                "entry": ", ".join(
                                    f"{{@skill {skill}}}"
                                    for skill in row.get("Skills").split(", ")
                                ),
                            }
                        ]
                        if pd.notnull(row.get("Skills")) and row.get("Skills")
                        else []
                    ),
                    *(
                        [
                            {
                                "type": "item",
                                "name": "Tool Proficiencies",
                                "entry": row.get("Tools"),
                            }
                        ]
                        if pd.notnull(row.get("Tools")) and row.get("Tools")
                        else []
                    ),
                    *(
                        [
                            {
                                "type": "item",
                                "name": "Languages",
                                "entry": ", ".join(
                                    f"{{@language {language}}}"
                                    for language in row.get("Languages").split(", ")
                                ),
                            }
                        ]
                        if pd.notnull(row.get("Languages"))
                        else []
                    ),
                    *(
                        [
                            {
                                "type": "item",
                                "name": "Equipment",
                                "entry": ", ".join(row.get("Items").split(", ")),
                            }
                        ]
                        if pd.notnull(row.get("Items")) and row.get("Items")
                        else []
                    ),
                ],
            },
            *(
                [
                    {
                        "name": row.get("Feature Name"),
                        "type": "entries",
                        "entries": [row.get("Feature")],
                        "data": {"isFeature": True},
                    }
                ]
                if pd.notnull(row.get("Feature Name"))
                else []
            ),
        ],
        **(
            {
                "startingEquipment": [
                    {
                        "_": [
                            {"special": item}
                            for item in row.get("Starting Equipment").split(", ")
                        ]
                    }
                ]
            }
            if pd.notnull(row.get("Starting Equipment"))
            and row.get("Starting Equipment")
            else {}
        ),
    }
