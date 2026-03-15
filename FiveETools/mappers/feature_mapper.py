from __future__ import annotations

from typing import Any

import inflection
import pandas as pd


def map_feature_entry_row(row: Any, *, df_class_features: pd.DataFrame) -> dict[str, Any]:
    name = row.get("Name")
    class_value = row.get("Class")
    classes = inflection.humanize(class_value) if pd.notnull(class_value) else ""
    entry = row.get("Entry")
    attribute = row.get("Attributes")

    sub_entries = [
        map_feature_entry_row(entry_row, df_class_features=df_class_features)
        for _, entry_row in df_class_features.iterrows()
        if pd.notnull(entry_row.get("Class"))
        and pd.notnull(entry_row.get("Parent"))
        and str(entry_row.get("Parent")).strip() == str(name).strip()
        and str(entry_row.get("Class")).strip() == str(classes).strip()
        and str(entry_row.get("Parent")).strip() != str(entry_row.get("Name")).strip()
    ]

    entries = [
        *(
            [entry]
            if not pd.isnull(row.get("Entry"))
            and not any(x.get("type") == "abilityDc" for x in sub_entries)
            else []
        ),
        *(
            (
                [
                    {
                        "type": "entries",
                        "name": "Spellcasting Ability",
                        "entries": [entry] + sub_entries,
                    }
                ]
                if any(x.get("type") == "abilityDc" for x in sub_entries)
                else [sub_entries]
            )
            if len(sub_entries) > 0
            else []
        ),
    ]

    return {
        **({"type": row.get("Type")} if not pd.isnull(row.get("Type")) else {"type": "entries"}),
        **({"name": name} if not pd.isnull(row.get("Parent")) else {}),
        **({"entries": entries} if len(entries) > 0 else {}),
        **({"attributes": attribute.split(", ")} if not pd.isnull(attribute) else {}),
    }


def map_feature_row(
    row: Any,
    *,
    json_source: str,
    df_class_features: pd.DataFrame,
) -> dict[str, Any]:
    name = row.get("Name")
    class_value = row.get("Class")
    classes = inflection.humanize(class_value) if pd.notnull(class_value) else ""
    level = int(row.get("Level"))
    entry = row.get("Entry")

    sub_entries = [
        map_feature_entry_row(entry_row, df_class_features=df_class_features)
        for _, entry_row in df_class_features.iterrows()
        if pd.notnull(entry_row.get("Class"))
        and pd.notnull(entry_row.get("Parent"))
        and str(entry_row.get("Parent")).strip() == str(name).strip()
        and str(entry_row.get("Class")).strip() == str(classes).strip()
    ]

    entries = [
        *(
            [entry]
            if not pd.isnull(entry)
            else ["Apparition unearthly spectral creepy uncanny wraith preternatural with"]
        ),
        *(
            (
                [
                    {
                        "type": "entries",
                        "name": "Spellcasting Ability",
                        "entries": [entry] + sub_entries,
                    }
                ]
                if len(sub_entries) > 0
                else [sub_entries]
            )
            if len(sub_entries) > 0
            else []
        ),
    ]

    return {
        **({"className": classes} if not pd.isnull(row.get("Class")) else {}),
        **({"name": name} if not pd.isnull(row.get("Name")) else {}),
        **({"level": level} if not pd.isnull(row.get("Level")) else {}),
        "source": json_source,
        "classSource": json_source,
        **({"entries": entries} if len(entries) > 0 else {}),
    }


def map_subclass_feature_row(
    row: Any,
    *,
    json_source: str,
    df_class_features: pd.DataFrame,
) -> dict[str, Any]:
    feature = map_feature_row(
        row,
        json_source=json_source,
        df_class_features=df_class_features,
    )
    feature["classSource"] = json_source
    feature["subclassSource"] = json_source
    feature["subclassShortName"] = row.get("Subclass")
    return feature
