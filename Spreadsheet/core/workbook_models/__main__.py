from __future__ import annotations

import argparse

from .registry import load_orimond_registry


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Pydantic sheet models for Orimond data.")
    parser.add_argument(
        "--source",
        choices=["google", "xlsx", "auto"],
        default="auto",
        help="Data source. `auto` tries Google first, then falls back to XLSX.",
    )
    parser.add_argument("--xlsx-path", default="Spreadsheet/Orimond.xlsx")
    parser.add_argument("--spreadsheet-id", default=None)
    parser.add_argument("--credentials-path", default=None)
    parser.add_argument(
        "--include-validation-sheets",
        action="store_true",
        help="Load validation sheets as records too.",
    )
    args = parser.parse_args()

    registry = load_orimond_registry(
        source=args.source,
        xlsx_path=args.xlsx_path,
        spreadsheet_id=args.spreadsheet_id or "1NBZGu29IfE1ZfAWO1Z6ShR5GMLMMbaSyS0m-46PSYm4",
        credentials_path=args.credentials_path,
    )

    print(f"Sheets discovered: {len(registry.available_sheets())}")
    print(f"Validation enums: {len(registry.validation_catalog.enums)}")

    records = registry.load_all(include_validation_sheets=args.include_validation_sheets, continue_on_error=True)
    registry.attach_relations(records)

    print("Record counts:")
    for sheet, rows in records.items():
        print(f"  - {sheet}: {len(rows)}")

    classes = records.get("Classes", [])
    if classes:
        example = classes[0]
        subclass_count = len(getattr(example, "subclasses", []))
        print(f"Example relation: Classes[0].subclasses -> {subclass_count} rows")


if __name__ == "__main__":
    main()
