from __future__ import annotations

from typing import Any, Literal

import pandas as pd

from FiveETools.core.fantasy import sources as fantasy_sources
from FiveETools.core.modern import sources as modern_sources
from FiveETools.mappers.species_mapper import (
    map_fantasy_species_row,
    map_modern_species_row,
)

Setting = Literal["fantasy", "modern"]

_SOURCE_CATALOGS = {
    "fantasy": fantasy_sources,
    "modern": modern_sources,
}
_MAPPERS = {
    "fantasy": map_fantasy_species_row,
    "modern": map_modern_species_row,
}
_SHEET_CACHES: dict[str, pd.DataFrame] = {}


def get_species_sheet(setting: Setting) -> pd.DataFrame:
    if setting not in _SHEET_CACHES:
        sheets_client = (
            fantasy_sources.fantasy_sheets
            if setting == "fantasy"
            else modern_sources.modern_sheets
        )
        _SHEET_CACHES[setting] = sheets_client.get_sheet_by_name("species")
    return _SHEET_CACHES[setting]


def row_to_species(
    row: Any, *, setting: Setting, df_species: pd.DataFrame
) -> dict[str, Any]:
    source_catalog = _SOURCE_CATALOGS[setting]
    mapper = _MAPPERS[setting]
    return mapper(
        row, df_species=df_species, default_source=source_catalog.DEFAULT_SOURCE
    )


def build_species_list(
    *,
    setting: Setting,
    source_code: str | None = None,
    df_species: pd.DataFrame | None = None,
) -> list[dict[str, Any]]:
    del source_code
    dataframe = df_species if df_species is not None else get_species_sheet(setting)
    return [
        row_to_species(row, setting=setting, df_species=dataframe)
        for _, row in dataframe.iterrows()
        if pd.notnull(row.get("Name"))
    ]


def build_races_list(
    *,
    setting: Setting,
    source_code: str | None = None,
    df_species: pd.DataFrame | None = None,
) -> list[dict[str, Any]]:
    return build_species_list(
        setting=setting,
        source_code=source_code,
        df_species=df_species,
    )


__all__ = [
    "build_races_list",
    "build_species_list",
    "get_species_sheet",
    "row_to_species",
]
