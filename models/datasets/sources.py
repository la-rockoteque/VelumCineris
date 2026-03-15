from __future__ import annotations

from Spreadsheet.core.lazy_exports import resolve_lazy_attr
from Spreadsheet.sheets import fantasy_sheets, modern_sheets

DEFAULT_SETTING = "fantasy"
SOURCES_SHEET_NAME = "sources"
DEFAULT_SOURCE = "ORIO"
DEFAULT_JSON_SOURCE = "ORIO"
DEFAULT_SOURCES = {
    "fantasy": DEFAULT_SOURCE,
    "modern": "VSTGCC",
}
DEFAULT_JSON_SOURCES = {
    "fantasy": DEFAULT_JSON_SOURCE,
    "modern": "VSTGCC",
}
_SHEETS_CLIENTS = {
    "fantasy": fantasy_sheets,
    "modern": modern_sheets,
}

_default_context: dict[str, tuple[str, str]] = {}
_source_context_cache: dict[tuple[str, str], tuple[str, str]] = {}
_attr_cache: dict[str, object] = {}


def normalize_setting(setting: str | None = None) -> str:
    normalized = str(setting or DEFAULT_SETTING).strip().lower()
    if normalized not in _SHEETS_CLIENTS:
        raise KeyError(f"Unknown dataset setting: {setting}")
    return normalized


def get_sheets_client(setting: str | None = None):
    return _SHEETS_CLIENTS[normalize_setting(setting)]


def get_sources_sheet(setting: str | None = None):
    """Load the shared sources sheet for the requested setting."""
    return get_sheets_client(setting).get_sheet_by_name(SOURCES_SHEET_NAME)


def resolve_source_context_for_setting(
    setting: str | None = None,
    source_code: str | None = None,
) -> tuple[str, str]:
    """Resolve source and json_source from the shared sources sheet."""
    setting_key = normalize_setting(setting)
    default_source = DEFAULT_SOURCES[setting_key]
    default_json_source = DEFAULT_JSON_SOURCES[setting_key]
    code = str(source_code).strip() if source_code else default_source
    cache_key = (setting_key, code)
    cached = _source_context_cache.get(cache_key)
    if cached is not None:
        return cached

    try:
        df_source = get_sources_sheet(setting_key)
        rows = df_source[df_source["Source"] == code]
        if not rows.empty:
            source_row = rows.iloc[0]
            json_source = str(source_row.get("json", "")).strip() or code
            _source_context_cache[cache_key] = (code, json_source)
            return _source_context_cache[cache_key]
    except Exception:
        pass

    if code == default_source:
        _source_context_cache[cache_key] = (code, default_json_source)
        return _source_context_cache[cache_key]

    _source_context_cache[cache_key] = (code, code)
    return _source_context_cache[cache_key]


def resolve_source_context(source_code: str = DEFAULT_SOURCE) -> tuple[str, str]:
    return resolve_source_context_for_setting(DEFAULT_SETTING, source_code)


def get_default_source_context(setting: str | None = None) -> tuple[str, str]:
    setting_key = normalize_setting(setting)
    if setting_key not in _default_context:
        _default_context[setting_key] = resolve_source_context_for_setting(setting_key)
    return _default_context[setting_key]


_RESOLVERS = {
    "source": lambda: get_default_source_context(DEFAULT_SETTING)[0],
    "json_source": lambda: get_default_source_context(DEFAULT_SETTING)[1],
}
_CACHED_ATTRS = {"source", "json_source"}


def __getattr__(name: str):
    return resolve_lazy_attr(
        module_name=__name__,
        attr_name=name,
        cache=_attr_cache,
        resolvers=_RESOLVERS,
        cached_attrs=_CACHED_ATTRS,
    )


__all__ = [
    "fantasy_sheets",
    "modern_sheets",
    "DEFAULT_SETTING",
    "SOURCES_SHEET_NAME",
    "DEFAULT_SOURCE",
    "DEFAULT_JSON_SOURCE",
    "DEFAULT_SOURCES",
    "DEFAULT_JSON_SOURCES",
    "normalize_setting",
    "get_sheets_client",
    "get_sources_sheet",
    "resolve_source_context_for_setting",
    "resolve_source_context",
    "get_default_source_context",
    "source",
    "json_source",
]
