from __future__ import annotations

import argparse
import json
import sys

from Spreadsheet.exports import write_json_report
from Spreadsheet.services import SpreadsheetService


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Spreadsheet utility CLI.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser(
        "list-sheets",
        help="List named content sheets for a content type.",
    )
    list_parser.add_argument(
        "--content-type",
        required=True,
        choices=["fantasy", "modern"],
        help="Content sheet type.",
    )

    preview_parser = subparsers.add_parser(
        "sheet-preview",
        help="Show a small preview from a named sheet.",
    )
    preview_parser.add_argument(
        "--content-type",
        required=True,
        choices=["fantasy", "modern"],
        help="Content sheet type.",
    )
    preview_parser.add_argument("--sheet-name", required=True, help="Named sheet key.")
    preview_parser.add_argument("--limit", type=int, default=10, help="Row preview size.")
    preview_parser.add_argument("--header", type=int, default=0, help="Pandas header row index.")

    summary_parser = subparsers.add_parser(
        "workbook-summary",
        help="Build a workbook-model summary report.",
    )
    summary_parser.add_argument(
        "--source",
        choices=["auto", "xlsx", "google"],
        default="auto",
        help="Workbook data source.",
    )
    summary_parser.add_argument(
        "--xlsx-path",
        default="Spreadsheet/Orimond.xlsx",
        help="Path used for xlsx/auto source mode.",
    )
    summary_parser.add_argument(
        "--spreadsheet-id",
        default=None,
        help="Optional Google spreadsheet ID override.",
    )
    summary_parser.add_argument(
        "--credentials-path",
        default=None,
        help="Optional Google credentials JSON path.",
    )
    summary_parser.add_argument(
        "--include-validation-sheets",
        action="store_true",
        help="Include validation sheets in loaded records.",
    )
    summary_parser.add_argument(
        "--out",
        default=None,
        help="Output report path (JSON).",
    )

    return parser


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()
    service = SpreadsheetService()

    try:
        if args.command == "list-sheets":
            names = service.list_sheets(content_type=args.content_type)
            print("\n".join(names))
            return 0

        if args.command == "sheet-preview":
            rows = service.sheet_preview(
                content_type=args.content_type,
                sheet_name=args.sheet_name,
                limit=args.limit,
                header=args.header,
            )
            print(json.dumps(rows, indent=2, ensure_ascii=True))
            return 0

        if args.command == "workbook-summary":
            summary = service.workbook_summary(
                source=args.source,
                xlsx_path=args.xlsx_path,
                spreadsheet_id=args.spreadsheet_id,
                credentials_path=args.credentials_path,
                include_validation_sheets=args.include_validation_sheets,
            )
            destination = write_json_report(
                summary,
                output_path=args.out,
                report_name="workbook_summary",
            )
            print(destination)
            return 0

        parser.error(f"Unsupported command: {args.command}")
        return 2
    except Exception as exc:
        print(f"Spreadsheet CLI error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

