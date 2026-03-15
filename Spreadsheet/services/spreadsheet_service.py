from __future__ import annotations

from typing import Any

from Spreadsheet.datasets import (
    load_registry,
    get_content_client,
    list_named_sheets,
)
from Spreadsheet.mappers import dataframe_preview, workbook_counts


class SpreadsheetService:
    def list_sheets(self, *, content_type: str) -> tuple[str, ...]:
        return list_named_sheets(content_type)

    def sheet_preview(
        self,
        *,
        content_type: str,
        sheet_name: str,
        limit: int = 10,
        header: int = 0,
    ) -> list[dict[str, Any]]:
        client = get_content_client(content_type)
        df = client.get_sheet_by_name(sheet_name, header=header)
        return dataframe_preview(df, limit=limit)

    def workbook_summary(
        self,
        *,
        source: str = "auto",
        xlsx_path: str = "Spreadsheet/Orimond.xlsx",
        spreadsheet_id: str | None = None,
        credentials_path: str | None = None,
        include_validation_sheets: bool = False,
    ) -> dict[str, Any]:
        registry = load_registry(
            source=source,
            xlsx_path=xlsx_path,
            spreadsheet_id=spreadsheet_id,
            credentials_path=credentials_path,
        )

        records = registry.load_all(
            include_validation_sheets=include_validation_sheets,
            continue_on_error=True,
        )
        registry.attach_relations(records)

        return {
            "available_sheets": registry.available_sheets(),
            "validation_enum_count": len(registry.validation_catalog.enums),
            "record_counts": workbook_counts(records),
        }

