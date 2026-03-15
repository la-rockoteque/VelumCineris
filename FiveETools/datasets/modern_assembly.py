from __future__ import annotations

from typing import Any

import pandas as pd

from FiveETools.core.modern import sources as source_catalog
from FiveETools.mappers.class_mapper import map_class_row
from FiveETools.mappers.feature_mapper import (
    map_feature_entry_row,
    map_feature_row,
    map_subclass_feature_row,
)
from FiveETools.mappers.subclass_mapper import map_subclass_row

_CLASSES_GID = "1924660120"
_CLASS_TABLES_GID = "193036738"
_CLASS_FEATURES_GID = "545140625"

_SHEET_CACHE: dict[str, pd.DataFrame] = {}


def _split_csv(value: Any) -> list[str]:
    if pd.isnull(value):
        return []
    return [part.strip() for part in str(value).split(",") if part.strip()]


def _to_int_or_empty(value: Any):
    if pd.isnull(value):
        return ""
    try:
        return int(value)
    except (TypeError, ValueError):
        return ""


def get_spells_sheet() -> pd.DataFrame:
    if "spells" not in _SHEET_CACHE:
        _SHEET_CACHE["spells"] = source_catalog.modern_sheets.get_sheet_by_name(
            "spells"
        )
    return _SHEET_CACHE["spells"]


def get_subclasses_sheet() -> pd.DataFrame:
    if "subclasses" not in _SHEET_CACHE:
        _SHEET_CACHE["subclasses"] = source_catalog.modern_sheets.get_sheet_by_name(
            "subclasses"
        )
    return _SHEET_CACHE["subclasses"]


def get_classes_sheet() -> pd.DataFrame:
    if "classes" not in _SHEET_CACHE:
        _SHEET_CACHE["classes"] = source_catalog.modern_sheets.get_sheet(
            _CLASSES_GID, header=1
        )
    return _SHEET_CACHE["classes"]


def get_class_tables_sheet() -> pd.DataFrame:
    if "class_tables" not in _SHEET_CACHE:
        _SHEET_CACHE["class_tables"] = source_catalog.modern_sheets.get_sheet(
            _CLASS_TABLES_GID,
            header=1,
        )
    return _SHEET_CACHE["class_tables"]


def get_class_features_sheet() -> pd.DataFrame:
    if "class_features" not in _SHEET_CACHE:
        _SHEET_CACHE["class_features"] = source_catalog.modern_sheets.get_sheet(
            _CLASS_FEATURES_GID,
            header=1,
        )
    return _SHEET_CACHE["class_features"]


def get_features_for_class(
    class_name,
    subclass_title=None,
    *,
    json_source: str | None = None,
    df_class_features: pd.DataFrame | None = None,
):
    del subclass_title
    if json_source is None:
        json_source = source_catalog.resolve_source_context(
            source_catalog.DEFAULT_SOURCE
        )[1]
    dataframe = (
        df_class_features
        if df_class_features is not None
        else get_class_features_sheet()
    )

    def get_feature_label(feature_row):
        name = feature_row.get("Name")
        level = int(feature_row.get("Level"))
        return f"{name}|{class_name}|{json_source}|{level}|{json_source}"

    return [
        get_feature_label(entry_row)
        for _, entry_row in dataframe.iterrows()
        if pd.notnull(entry_row.get("Class"))
        and pd.notnull(entry_row.get("Name"))
        and pd.notnull(entry_row.get("Level"))
        and pd.isnull(entry_row.get("Parent"))
        and str(entry_row.get("Class")) == str(class_name)
    ]


def get_features_for_subclass(
    class_name,
    subclass_name,
    *,
    json_source: str | None = None,
    df_class_features: pd.DataFrame | None = None,
):
    if json_source is None:
        json_source = source_catalog.resolve_source_context(
            source_catalog.DEFAULT_SOURCE
        )[1]
    dataframe = (
        df_class_features
        if df_class_features is not None
        else get_class_features_sheet()
    )

    def get_feature_label(feature_row):
        name = feature_row.get("Name")
        level = int(feature_row.get("Level"))
        return (
            f"{name}|{class_name}|{json_source}|{subclass_name}|"
            f"{json_source}|{level}|{json_source}"
        )

    return [
        get_feature_label(entry_row)
        for _, entry_row in dataframe.iterrows()
        if pd.notnull(entry_row.get("Class"))
        and pd.notnull(entry_row.get("Name"))
        and str(entry_row.get("Subclass")) == subclass_name
    ]


def to_table(class_name: str, *, df_class_tables: pd.DataFrame | None = None):
    dataframe = (
        df_class_tables if df_class_tables is not None else get_class_tables_sheet()
    )
    header_rows = dataframe.loc[dataframe["Class"] == class_name]
    if header_rows.empty:
        return {"colLabels": [], "rows": []}
    header = header_rows.iloc[0]

    def process(table_row):
        proficiency = _to_int_or_empty(table_row.get("Proficiency Bonus"))
        known_spells = _to_int_or_empty(table_row.get("Spells Known"))
        max_spell_level = _to_int_or_empty(table_row.get("Max Spell Level"))
        points = _to_int_or_empty(table_row.get("Points"))
        spell_slots = _to_int_or_empty(table_row.get("Total spell slots"))
        feature_1 = _to_int_or_empty(table_row.get("Feature 1"))
        return [
            *(
                [proficiency]
                if not pd.isnull(table_row.get("Proficiency Bonus"))
                else []
            ),
            *([known_spells] if not pd.isnull(table_row.get("Spells Known")) else []),
            *(
                [max_spell_level]
                if not pd.isnull(table_row.get("Max Spell Level"))
                else []
            ),
            *([points] if not pd.isnull(table_row.get("Points")) else []),
            *(
                [spell_slots]
                if not pd.isnull(table_row.get("Total spell slots"))
                else []
            ),
            *([feature_1] if not pd.isnull(table_row.get("Feature 1")) else []),
        ]

    labels = [
        *(
            [f"{{@filter Proficiency Bonus|value|class={class_name}}}"]
            if not pd.isnull(header.get("Proficiency Bonus"))
            else []
        ),
        *(
            [f"{{@filter Spells Known|value|class={class_name}}}"]
            if not pd.isnull(header.get("Spells Known"))
            else []
        ),
        *(
            [f"{{@filter Max Spell Level|value|class={class_name}}}"]
            if not pd.isnull(header.get("Max Spell Level"))
            else []
        ),
        *(
            [f"{{@filter Points|value|class={class_name}}}"]
            if not pd.isnull(header.get("Points"))
            else []
        ),
        *(
            [f"{{@filter Total spell slots|value|class={class_name}}}"]
            if not pd.isnull(header.get("Total spell slots"))
            else []
        ),
        *(
            [f"{{@filter {header.get('Feature 1 Name')}|value|class={class_name}}}"]
            if not pd.isnull(header.get("Feature 1 Name"))
            else []
        ),
    ]

    rows = [
        process(table_row)
        for _, table_row in dataframe.iterrows()
        if pd.notnull(table_row.get("Class"))
        and str(table_row.get("Class")).strip() == class_name
    ]

    return {"colLabels": labels, "rows": rows}


def to_spell_progression_table(
    class_name: str, *, df_class_tables: pd.DataFrame | None = None
):
    dataframe = (
        df_class_tables if df_class_tables is not None else get_class_tables_sheet()
    )
    labels = [
        f"{{@filter {level}|spells|level={level[0]}|class={class_name}}}"
        for level in ["1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th"]
    ]

    rows = [
        [
            table_row.get("1"),
            table_row.get("2"),
            table_row.get("3"),
            table_row.get("4"),
            table_row.get("5"),
            table_row.get("6"),
            table_row.get("7"),
            table_row.get("8"),
            table_row.get("9"),
        ]
        for _, table_row in dataframe.iterrows()
        if pd.notnull(table_row.get("Class"))
        and str(table_row.get("Class")).strip() == class_name
    ]

    return {"title": "Spell Slots per Spell Level", "colLabels": labels, "rows": rows}


def row_to_class(
    row,
    *,
    source: str,
    json_source: str,
    df_spells: pd.DataFrame,
    df_subclasses: pd.DataFrame,
    df_class_tables: pd.DataFrame,
    df_class_features: pd.DataFrame,
):
    return map_class_row(
        row,
        source=source,
        json_source=json_source,
        default_source=source_catalog.DEFAULT_SOURCE,
        df_spells=df_spells,
        df_subclasses=df_subclasses,
        df_class_tables=df_class_tables,
        df_class_features=df_class_features,
        split_csv=_split_csv,
        to_table_fn=to_table,
        to_spell_progression_table_fn=to_spell_progression_table,
        get_features_for_class_fn=get_features_for_class,
    )


def row_to_subclass(row, *, json_source: str, df_class_features: pd.DataFrame):
    subclass_name = row.get("Name")
    class_name = row.get("Class")
    features = get_features_for_subclass(
        class_name,
        subclass_name,
        json_source=json_source,
        df_class_features=df_class_features,
    )
    return map_subclass_row(row, json_source=json_source, features=features)


def row_to_feature_entries(row, *, df_class_features: pd.DataFrame):
    return map_feature_entry_row(row, df_class_features=df_class_features)


def row_to_features(row, *, json_source: str, df_class_features: pd.DataFrame):
    return map_feature_row(
        row,
        json_source=json_source,
        df_class_features=df_class_features,
    )


def row_to_subclass_features(row, *, json_source: str, df_class_features: pd.DataFrame):
    return map_subclass_feature_row(
        row,
        json_source=json_source,
        df_class_features=df_class_features,
    )


def build_classes_list(
    source_code: str | None = None,
    *,
    df_classes: pd.DataFrame | None = None,
    df_spells: pd.DataFrame | None = None,
    df_subclasses: pd.DataFrame | None = None,
    df_class_tables: pd.DataFrame | None = None,
    df_class_features: pd.DataFrame | None = None,
) -> list[dict[str, Any]]:
    effective_source_code = source_code or source_catalog.DEFAULT_SOURCE
    source, json_source = source_catalog.resolve_source_context(effective_source_code)

    classes = df_classes if df_classes is not None else get_classes_sheet()
    spells = df_spells if df_spells is not None else get_spells_sheet()
    subclasses = df_subclasses if df_subclasses is not None else get_subclasses_sheet()
    class_tables = (
        df_class_tables if df_class_tables is not None else get_class_tables_sheet()
    )
    class_features = (
        df_class_features
        if df_class_features is not None
        else get_class_features_sheet()
    )

    return [
        row_to_class(
            row,
            source=source,
            json_source=json_source,
            df_spells=spells,
            df_subclasses=subclasses,
            df_class_tables=class_tables,
            df_class_features=class_features,
        )
        for _, row in classes.iterrows()
        if pd.notnull(row.get("Name"))
        and str(row.get("Name")).strip() != ""
        and row.get("Source") == source
    ]


def build_subclasses_list(
    source_code: str | None = None,
    *,
    df_subclasses: pd.DataFrame | None = None,
    df_class_features: pd.DataFrame | None = None,
) -> list[dict[str, Any]]:
    effective_source_code = source_code or source_catalog.DEFAULT_SOURCE
    source, json_source = source_catalog.resolve_source_context(effective_source_code)
    subclasses = df_subclasses if df_subclasses is not None else get_subclasses_sheet()
    class_features = (
        df_class_features
        if df_class_features is not None
        else get_class_features_sheet()
    )

    return [
        row_to_subclass(row, json_source=json_source, df_class_features=class_features)
        for _, row in subclasses.iterrows()
        if pd.notnull(row.get("Name"))
        and str(row.get("Name")).strip() != ""
        and row.get("Source") == source
    ]


def build_features_list(
    source_code: str | None = None,
    *,
    df_class_features: pd.DataFrame | None = None,
) -> list[dict[str, Any]]:
    effective_source_code = source_code or source_catalog.DEFAULT_SOURCE
    source, json_source = source_catalog.resolve_source_context(effective_source_code)
    class_features = (
        df_class_features
        if df_class_features is not None
        else get_class_features_sheet()
    )

    features = [
        row_to_features(row, json_source=json_source, df_class_features=class_features)
        for _, row in class_features.iterrows()
        if pd.notnull(row.get("Name"))
        and pd.isnull(row.get("Parent"))
        and row.get("Source") == source
        and pd.isnull(row.get("Subclass"))
    ]

    dedup: dict[str, dict[str, Any]] = {}
    for item in features:
        key = f"{item.get('className')}\0{item.get('name')}\1{item.get('level')}"
        dedup[key] = item
    return list(dedup.values())


def build_sub_class_features_list(
    source_code: str | None = None,
    *,
    df_class_features: pd.DataFrame | None = None,
) -> list[dict[str, Any]]:
    effective_source_code = source_code or source_catalog.DEFAULT_SOURCE
    source, json_source = source_catalog.resolve_source_context(effective_source_code)
    class_features = (
        df_class_features
        if df_class_features is not None
        else get_class_features_sheet()
    )

    return [
        row_to_subclass_features(
            row,
            json_source=json_source,
            df_class_features=class_features,
        )
        for _, row in class_features.iterrows()
        if pd.notnull(row.get("Name"))
        and pd.isnull(row.get("Parent"))
        and row.get("Source") == source
        and pd.notnull(row.get("Subclass"))
    ]


__all__ = [
    "build_classes_list",
    "build_features_list",
    "build_sub_class_features_list",
    "build_subclasses_list",
    "get_class_features_sheet",
    "get_class_tables_sheet",
    "get_classes_sheet",
    "get_features_for_class",
    "get_features_for_subclass",
    "get_spells_sheet",
    "get_subclasses_sheet",
    "row_to_class",
    "row_to_feature_entries",
    "row_to_features",
    "row_to_subclass",
    "row_to_subclass_features",
    "to_spell_progression_table",
    "to_table",
]
