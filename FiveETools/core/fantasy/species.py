from __future__ import annotations

from FiveETools.datasets import species as species_dataset
from FiveETools.core.fantasy import sources as source_catalog
from Spreadsheet.core.lazy_exports import resolve_lazy_attr

_cache: dict[str, object] = {}


def get_species_sheet():
    return species_dataset.get_species_sheet("fantasy")


def row_to_species(row, *, df_species):
    return species_dataset.row_to_species(row, setting="fantasy", df_species=df_species)


def build_species_list(source_code: str | None = None) -> list[dict]:
    return species_dataset.build_species_list(
        setting="fantasy", source_code=source_code
    )


def build_races_list(source_code: str | None = None) -> list[dict]:
    return species_dataset.build_races_list(setting="fantasy", source_code=source_code)


_RESOLVERS = {
    "source": lambda: source_catalog.resolve_source_context(
        source_catalog.DEFAULT_SOURCE
    )[0],
    "json_source": lambda: source_catalog.resolve_source_context(
        source_catalog.DEFAULT_SOURCE
    )[1],
    "species_list": build_species_list,
    "races_list": build_races_list,
}
_CACHED_ATTRS = {"species_list", "races_list"}


def __getattr__(name: str):
    return resolve_lazy_attr(
        module_name=__name__,
        attr_name=name,
        cache=_cache,
        resolvers=_RESOLVERS,
        cached_attrs=_CACHED_ATTRS,
    )


__all__ = [
    "get_species_sheet",
    "row_to_species",
    "build_species_list",
    "build_races_list",
    "source",
    "json_source",
    "species_list",
    "races_list",
]
