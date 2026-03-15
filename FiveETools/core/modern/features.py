from __future__ import annotations

from FiveETools.datasets import modern_assembly
from FiveETools.core.modern import sources as source_catalog
from Spreadsheet.core.lazy_exports import resolve_lazy_attr

_cache: dict[str, object] = {}


def get_class_features_sheet():
    return modern_assembly.get_class_features_sheet()


def row_to_feature_entries(row, **kwargs):
    return modern_assembly.row_to_feature_entries(row, **kwargs)


def row_to_features(row, **kwargs):
    return modern_assembly.row_to_features(row, **kwargs)


def row_to_subclass_features(row, **kwargs):
    return modern_assembly.row_to_subclass_features(row, **kwargs)


def build_features_list(source_code: str | None = None) -> list[dict]:
    return modern_assembly.build_features_list(source_code=source_code)


def build_sub_class_features_list(source_code: str | None = None) -> list[dict]:
    return modern_assembly.build_sub_class_features_list(source_code=source_code)


_RESOLVERS = {
    "source": lambda: source_catalog.resolve_source_context(
        source_catalog.DEFAULT_SOURCE
    )[0],
    "json_source": lambda: source_catalog.resolve_source_context(
        source_catalog.DEFAULT_SOURCE
    )[1],
    "features_list": build_features_list,
    "sub_class_features_list": build_sub_class_features_list,
}
_CACHED_ATTRS = {"features_list", "sub_class_features_list"}


def __getattr__(name: str):
    return resolve_lazy_attr(
        module_name=__name__,
        attr_name=name,
        cache=_cache,
        resolvers=_RESOLVERS,
        cached_attrs=_CACHED_ATTRS,
    )


__all__ = [
    "get_class_features_sheet",
    "row_to_feature_entries",
    "row_to_features",
    "row_to_subclass_features",
    "build_features_list",
    "build_sub_class_features_list",
    "source",
    "json_source",
    "features_list",
    "sub_class_features_list",
]
