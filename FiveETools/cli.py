from __future__ import annotations

import argparse


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="FiveETools utility CLI.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    export_parser = subparsers.add_parser("export", help="Build a 5etools compendium JSON export.")
    export_parser.add_argument(
        "--setting",
        choices=["fantasy", "modern"],
        required=True,
        help="Content setting to export.",
    )
    export_parser.add_argument(
        "--source",
        default=None,
        help="Optional source code override (e.g. ORIO, VSTGCC).",
    )
    export_parser.add_argument(
        "--out",
        default=None,
        help="Output file path. Defaults to FiveETools/out/Velum_Cineris;<source>.json.",
    )
    return parser


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()

    if args.command == "export":
        from FiveETools.services import FiveEToolsExportService

        service = FiveEToolsExportService()
        output_path = service.export_to_file(
            setting=args.setting,
            source_code=args.source,
            output_path=args.out,
        )
        print(output_path)
        return 0

    parser.error(f"Unsupported command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
