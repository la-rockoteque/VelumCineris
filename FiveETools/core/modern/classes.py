from __future__ import annotations

from FiveETools.datasets import modern_assembly
from FiveETools.core.modern import sources as source_catalog
from Spreadsheet.core.lazy_exports import resolve_lazy_attr

_cache: dict[str, object] = {}


def get_spells_sheet():
    return modern_assembly.get_spells_sheet()


def get_subclasses_sheet():
    return modern_assembly.get_subclasses_sheet()


def get_classes_sheet():
    return modern_assembly.get_classes_sheet()


def get_class_tables_sheet():
    return modern_assembly.get_class_tables_sheet()


def get_class_features_sheet():
    return modern_assembly.get_class_features_sheet()


def get_features_for_class(class_name, subclass_title=None, **kwargs):
    return modern_assembly.get_features_for_class(
        class_name,
        subclass_title,
        **kwargs,
    )


def to_table(class_name: str, **kwargs):
    return modern_assembly.to_table(class_name, **kwargs)


def to_spell_progression_table(class_name: str, **kwargs):
    return modern_assembly.to_spell_progression_table(class_name, **kwargs)


def row_to_class(row, **kwargs):
    return modern_assembly.row_to_class(row, **kwargs)


def build_classes_list(source_code: str | None = None) -> list[dict]:
    return modern_assembly.build_classes_list(source_code=source_code)


_RESOLVERS = {
    "source": lambda: source_catalog.resolve_source_context(
        source_catalog.DEFAULT_SOURCE
    )[0],
    "json_source": lambda: source_catalog.resolve_source_context(
        source_catalog.DEFAULT_SOURCE
    )[1],
    "classes_list": build_classes_list,
}
_CACHED_ATTRS = {"classes_list"}


def __getattr__(name: str):
    return resolve_lazy_attr(
        module_name=__name__,
        attr_name=name,
        cache=_cache,
        resolvers=_RESOLVERS,
        cached_attrs=_CACHED_ATTRS,
    )


__all__ = [
    "get_spells_sheet",
    "get_subclasses_sheet",
    "get_classes_sheet",
    "get_class_tables_sheet",
    "get_class_features_sheet",
    "get_features_for_class",
    "to_table",
    "to_spell_progression_table",
    "row_to_class",
    "build_classes_list",
    "source",
    "json_source",
    "classes_list",
]
