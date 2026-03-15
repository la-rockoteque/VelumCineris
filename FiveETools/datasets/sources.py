from __future__ import annotations

from typing import Any

import inflection
import pandas as pd

from models.datasets import sources as shared_sources

DEFAULT_SETTING = shared_sources.DEFAULT_SETTING
SOURCES_SHEET_NAME = shared_sources.SOURCES_SHEET_NAME
DEFAULT_SOURCES = shared_sources.DEFAULT_SOURCES
DEFAULT_JSON_SOURCES = shared_sources.DEFAULT_JSON_SOURCES
fantasy_sheets = shared_sources.fantasy_sheets
modern_sheets = shared_sources.modern_sheets

_FULL_SOURCE_CACHE: dict[tuple[str, str], str] = {}
_SOURCES_CACHE: dict[str, list[dict[str, Any]]] = {}


def normalize_setting(setting: str | None = None) -> str:
    return shared_sources.normalize_setting(setting)


def get_sheets_client(setting: str | None = None):
    return shared_sources.get_sheets_client(setting)


def get_sources_sheet(setting: str | None = None):
    return shared_sources.get_sources_sheet(setting)


def resolve_source_context(
    *, setting: str | None = None, source_code: str | None = None
) -> tuple[str, str]:
    return shared_sources.resolve_source_context_for_setting(setting, source_code)


def get_default_source_context(setting: str | None = None) -> tuple[str, str]:
    return shared_sources.get_default_source_context(setting)


def get_full_source(
    *, setting: str | None = None, source_code: str | None = None
) -> str:
    setting_key = normalize_setting(setting)
    code, _ = resolve_source_context(setting=setting_key, source_code=source_code)
    cache_key = (setting_key, code)
    cached = _FULL_SOURCE_CACHE.get(cache_key)
    if cached is not None:
        return cached

    full_source = ""
    try:
        df_source = get_sources_sheet(setting_key)
        rows = df_source[df_source["Source"] == code]
        if not rows.empty:
            full_source = str(rows.iloc[0].get("Full", "")).strip()
    except Exception:
        pass

    _FULL_SOURCE_CACHE[cache_key] = full_source
    return full_source


def list_sources(*, setting: str | None = None) -> list[dict[str, Any]]:
    setting_key = normalize_setting(setting)
    cached = _SOURCES_CACHE.get(setting_key)
    if cached is not None:
        return cached

    records: list[dict[str, Any]] = []
    try:
        df_source = get_sources_sheet(setting_key)
        for _, row in df_source.iterrows():
            if pd.isnull(row.get("Full")):
                continue
            json_source = str(row.get("json", "")).strip()
            if not json_source:
                continue
            records.append(
                {
                    "json": json_source,
                    "abbreviation": row.get("Source"),
                    "full": row.get("Full"),
                    "url": (
                        "https://raw.githubusercontent.com/la-rockoteque/Vestigium/refs/heads/main/"
                        f"Velum_Cineris;{inflection.underscore(json_source)}.json"
                    ),
                    "authors": ["Velum Cineris"],
                    "version": "1.0",
                }
            )
    except Exception:
        default_source = DEFAULT_SOURCES[setting_key]
        _, default_json_source = resolve_source_context(
            setting=setting_key,
            source_code=default_source,
        )
        records = [
            {
                "json": default_json_source,
                "abbreviation": default_source,
                "full": "",
                "url": (
                    "https://raw.githubusercontent.com/la-rockoteque/Vestigium/refs/heads/main/"
                    f"Velum_Cineris;{inflection.underscore(default_json_source)}.json"
                ),
                "authors": ["Velum Cineris"],
                "version": "1.0",
            }
        ]

    _SOURCES_CACHE[setting_key] = records
    return records


__all__ = [
    "DEFAULT_SETTING",
    "DEFAULT_SOURCES",
    "DEFAULT_JSON_SOURCES",
    "SOURCES_SHEET_NAME",
    "fantasy_sheets",
    "modern_sheets",
    "normalize_setting",
    "get_sheets_client",
    "get_sources_sheet",
    "resolve_source_context",
    "get_default_source_context",
    "get_full_source",
    "list_sources",
]
