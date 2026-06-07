from __future__ import annotations

from typing import Any

import pandas as pd


def _present(value: Any) -> bool:
    return value is not None and not pd.isna(value) and bool(str(value).strip())


def _split_choices(value: Any) -> list[str]:
    if not _present(value):
        return []
    return [
        part.strip() for part in str(value).replace(",", ";").split(";") if part.strip()
    ]


def _rule_bullets(value: Any) -> list[dict[str, Any]]:
    entries = []
    for bullet in _split_choices(value):
        name, separator, text = bullet.partition("::")
        entries.append(
            {
                "name": name.strip(),
                "type": "entries",
                "entries": [text.strip()] if separator and text.strip() else [],
            }
        )
    return entries


def map_background_row(row: Any, *, source: str, json_source: str) -> dict[str, Any]:
    del source
    name = row.get("Background") if _present(row.get("Background")) else row.get("Name")
    skills = (
        _split_choices(row.get("Skills"))
        if _present(row.get("Skills"))
        else _split_choices(row.get("Skill Proficiency Choice"))
    )
    tools = (
        row.get("Tools")
        if _present(row.get("Tools"))
        else row.get("Tool Proficiency Choice")
    )
    languages = (
        _split_choices(row.get("Languages"))
        if _present(row.get("Languages"))
        else _split_choices(row.get("Language Choice"))
    )
    equipment = (
        row.get("Items") if _present(row.get("Items")) else row.get("Equipment Text")
    )
    feature = (
        row.get("Feature")
        if _present(row.get("Feature"))
        else row.get("Feature Rules Text")
    )
    feature_name = row.get("Feature Name")

    items = []
    if skills:
        items.append(
            {
                "type": "item",
                "name": "Skill Proficiencies",
                "entry": ", ".join(f"{{@skill {skill}}}" for skill in skills),
            }
        )
    if _present(tools):
        items.append(
            {"type": "item", "name": "Tool Proficiencies", "entry": str(tools)}
        )
    if languages:
        items.append(
            {
                "type": "item",
                "name": "Languages",
                "entry": ", ".join(
                    f"{{@language {language}}}" for language in languages
                ),
            }
        )
    if _present(equipment):
        items.append({"type": "item", "name": "Equipment", "entry": str(equipment)})

    entries: list[dict[str, Any]] = []
    if items:
        entries.append({"type": "list", "style": "list-hang-notitle", "items": items})
    if _present(feature_name):
        entries.append(
            {
                "name": str(feature_name),
                "type": "entries",
                "entries": [str(feature)] if _present(feature) else [],
                "data": {"isFeature": True},
            }
        )
    entries.extend(_rule_bullets(row.get("Feature Bullets")))

    return {
        "name": str(name).strip() if _present(name) else "Unnamed Background",
        "source": json_source,
        **(
            {"skillProficiencies": [{skill.lower(): True for skill in skills}]}
            if skills
            else {}
        ),
        "entries": entries,
        **(
            {
                "startingEquipment": [
                    {
                        "_": [
                            {"special": item}
                            for item in _split_choices(row.get("Starting Equipment"))
                        ]
                    }
                ]
            }
            if _present(row.get("Starting Equipment"))
            else {}
        ),
    }
