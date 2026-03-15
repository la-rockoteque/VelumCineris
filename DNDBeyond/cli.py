from __future__ import annotations

import argparse
import sys

from DNDBeyond.datasets import list_entity_types
from DNDBeyond.exports import write_payloads
from DNDBeyond.services import DnDBeyondPayloadService


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="D&D Beyond utility CLI.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    export_parser = subparsers.add_parser(
        "export-payloads",
        help="Build offline D&D Beyond payload JSON from FiveETools content.",
    )
    export_parser.add_argument(
        "--entity",
        required=True,
        choices=list_entity_types(),
        help="Entity type to convert.",
    )
    export_parser.add_argument(
        "--setting",
        required=True,
        choices=["fantasy", "modern"],
        help="Content setting.",
    )
    export_parser.add_argument(
        "--source",
        default=None,
        help="Optional source override (e.g. ORIO, VSTGCC).",
    )
    export_parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Optional max number of entities to convert.",
    )
    export_parser.add_argument(
        "--include-spell-extras",
        action="store_true",
        help="Include extracted spell extras in payload records.",
    )
    export_parser.add_argument(
        "--out",
        default=None,
        help="Output path (defaults to DNDBeyond/out/<entity>_payloads_<setting>.json).",
    )

    return parser


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()

    if args.command == "export-payloads":
        service = DnDBeyondPayloadService()
        try:
            payloads = service.build_payloads(
                entity_type=args.entity,
                setting=args.setting,
                source_code=args.source,
                limit=args.limit,
                include_spell_extras=args.include_spell_extras,
            )
            destination = write_payloads(
                payloads,
                output_path=args.out,
                entity_type=args.entity,
                setting=args.setting,
            )
            print(destination)
            return 0
        except Exception as exc:
            print(f"Failed to export payloads: {exc}", file=sys.stderr)
            return 1

    parser.error(f"Unsupported command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
