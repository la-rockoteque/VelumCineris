from __future__ import annotations

from typing import cast

from FiveETools.core.modern import sources as source_catalog
from FiveETools.datasets.json_loader import build_mapped_rows
from FiveETools.mappers.feat_mapper import map_feat_row
from Spreadsheet.core.lazy_exports import resolve_lazy_attr
from Spreadsheet.core.converters.feat import FeatConverter
from models.datasets import get_converter as get_dataset_converter
from models.datasets import load_dataset
from models.entities.feat import Feat

_cache: dict[str, object] = {}


def row_to_feat(row, *, json_source: str):
    return map_feat_row(row, json_source=json_source)


def get_converter() -> FeatConverter:
    return cast(FeatConverter, get_dataset_converter("feats", setting="modern"))


def build_feat_list(source_code: str | None = None) -> list[dict]:
    return build_mapped_rows(
        sheets_client=source_catalog.modern_sheets,
        sheet_name="feats",
        source_code=source_code,
        default_source=source_catalog.DEFAULT_SOURCE,
        resolve_source_context=source_catalog.resolve_source_context,
        row_mapper=row_to_feat,
        name_column="Name",
        filter_by_source=True,
    )


def build_feat_pydantic(source_code: str | None = None) -> list[Feat]:
    return cast(
        list[Feat], load_dataset("feats", source_code=source_code, setting="modern")
    )


_RESOLVERS = {
    "source": lambda: source_catalog.resolve_source_context(
        source_catalog.DEFAULT_SOURCE
    )[0],
    "json_source": lambda: source_catalog.resolve_source_context(
        source_catalog.DEFAULT_SOURCE
    )[1],
    "feat_list": build_feat_list,
    "converter": get_converter,
    "feat_pydantic": build_feat_pydantic,
}
_CACHED_ATTRS = {"feat_list", "feat_pydantic"}


def __getattr__(name: str):
    return resolve_lazy_attr(
        module_name=__name__,
        attr_name=name,
        cache=_cache,
        resolvers=_RESOLVERS,
        cached_attrs=_CACHED_ATTRS,
    )


__all__ = [
    "row_to_feat",
    "get_converter",
    "build_feat_list",
    "build_feat_pydantic",
    "source",
    "json_source",
    "feat_list",
    "converter",
    "feat_pydantic",
]
