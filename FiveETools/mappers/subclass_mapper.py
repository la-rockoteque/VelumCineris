from __future__ import annotations

from typing import Any


def map_subclass_row(
    row: Any,
    *,
    json_source: str,
    features: list[str],
) -> dict[str, Any]:
    subclass_name = row.get("Name")
    class_name = row.get("Class")
    return {
        "name": subclass_name,
        "source": json_source,
        "className": class_name,
        "classSource": json_source,
        "shortName": subclass_name,
        "subclassFeatures": features,
    }
