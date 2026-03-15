from __future__ import annotations

from FiveETools.datasets import modern_assembly
from FiveETools.core.modern import sources as source_catalog
from Spreadsheet.core.lazy_exports import resolve_lazy_attr

_cache: dict[str, object] = {}


def get_subclasses_sheet():
    return modern_assembly.get_subclasses_sheet()


def get_class_features_sheet():
    return modern_assembly.get_class_features_sheet()


def get_features_for_subclass(class_name, subclass_name, **kwargs):
    return modern_assembly.get_features_for_subclass(
        class_name, subclass_name, **kwargs
    )


def row_to_subclass(row, **kwargs):
    return modern_assembly.row_to_subclass(row, **kwargs)


def build_subclasses_list(source_code: str | None = None) -> list[dict]:
    return modern_assembly.build_subclasses_list(source_code=source_code)


_RESOLVERS = {
    "source": lambda: source_catalog.resolve_source_context(
        source_catalog.DEFAULT_SOURCE
    )[0],
    "json_source": lambda: source_catalog.resolve_source_context(
        source_catalog.DEFAULT_SOURCE
    )[1],
    "subclasses_list": build_subclasses_list,
}
_CACHED_ATTRS = {"subclasses_list"}


def __getattr__(name: str):
    return resolve_lazy_attr(
        module_name=__name__,
        attr_name=name,
        cache=_cache,
        resolvers=_RESOLVERS,
        cached_attrs=_CACHED_ATTRS,
    )


__all__ = [
    "get_subclasses_sheet",
    "get_class_features_sheet",
    "get_features_for_subclass",
    "row_to_subclass",
    "build_subclasses_list",
    "source",
    "json_source",
    "subclasses_list",
]
