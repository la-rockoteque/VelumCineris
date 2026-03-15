from __future__ import annotations

from pathlib import Path
from typing import Any

from FiveETools.datasets import get_dataset_module
from FiveETools.exports.compendium import (
    build_compendium_document,
    build_default_output_filename,
    write_compendium_document,
)


class FiveEToolsExportService:
    def build_document(
        self,
        *,
        setting: str,
        source_code: str | None = None,
    ) -> tuple[dict[str, Any], str]:
        dataset_module = get_dataset_module(setting)
        source_catalog = dataset_module.get_source_catalog()
        source_code = source_code or source_catalog.DEFAULT_SOURCE
        _, json_source = source_catalog.resolve_source_context(source_code)
        sections = dataset_module.build_sections(source_code=source_code)
        document = build_compendium_document(
            sources=source_catalog.list_sources(),
            sections=sections,
        )
        return document, json_source

    def export_to_file(
        self,
        *,
        setting: str,
        source_code: str | None = None,
        output_path: str | Path | None = None,
    ) -> Path:
        document, json_source = self.build_document(
            setting=setting,
            source_code=source_code,
        )
        destination = (
            Path(output_path)
            if output_path is not None
            else Path("FiveETools/out") / build_default_output_filename(json_source)
        )
        return write_compendium_document(document, destination)
