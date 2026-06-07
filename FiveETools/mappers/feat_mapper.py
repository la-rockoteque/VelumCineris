from __future__ import annotations

from typing import Any


def _present(value: Any) -> bool:
    return value is not None and str(value).strip() not in {"", "nan", "None"}


def _rule_bullets(value: Any) -> list[str]:
    if not _present(value):
        return []
    entries = []
    for bullet in str(value).split(";"):
        name, separator, text = bullet.strip().partition("::")
        if not name:
            continue
        entries.append(
            f"### {name.strip()}\n{text.strip()}" if separator else name.strip()
        )
    return entries


def map_feat_row(row: Any, *, json_source: str) -> dict[str, Any]:
    entries = []
    prerequisite = row.get("Prerequisite Text")
    if _present(prerequisite):
        entries.append(f"*Prerequisite: {str(prerequisite).strip()}*")

    rules_text = row.get("Rules Text")
    if _present(rules_text):
        entries.append(str(rules_text).strip())
    entries.extend(_rule_bullets(row.get("Rules Bullets")))

    if not entries and "Feat" in row.index:
        feat_pos = row.index.get_loc("Feat")
        flavor_text = row.get("Flavor Text")
        if _present(flavor_text):
            entries.append(str(flavor_text).strip())
        entries.extend(str(value) for value in row.iloc[feat_pos:].dropna().tolist())

    name = row.get("Name")
    return {
        "name": str(name).strip().lower() if _present(name) else "unnamed feat",
        "source": json_source,
        "entries": entries,
    }
