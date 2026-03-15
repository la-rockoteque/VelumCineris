from __future__ import annotations

import argparse
import sys

from Homebrewery.datasets import list_entity_types
from Homebrewery.exports import write_markdown
from Homebrewery.services import HomebreweryMarkdownService


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Homebrewery utility CLI.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    export_parser = subparsers.add_parser(
        "export-markdown",
        help="Build markdown from FiveETools entities.",
    )
    export_parser.add_argument(
        "--entity",
        required=True,
        choices=list_entity_types(),
        help="Entity type to render.",
    )
    export_parser.add_argument(
        "--setting",
        default="modern",
        choices=["modern"],
        help="Content setting.",
    )
    export_parser.add_argument(
        "--source",
        default=None,
        help="Optional source override (e.g. VSTGCC).",
    )
    export_parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Optional max number of entities to render.",
    )
    export_parser.add_argument(
        "--title",
        default=None,
        help="Optional markdown title.",
    )
    export_parser.add_argument(
        "--out",
        default=None,
        help="Output path (defaults to Homebrewery/core/markdown/<entity>_<setting>.txt).",
    )

    return parser


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()

    if args.command == "export-markdown":
        service = HomebreweryMarkdownService()
        try:
            markdown = service.build_markdown(
                entity_type=args.entity,
                setting=args.setting,
                source_code=args.source,
                limit=args.limit,
                title=args.title,
            )
            destination = write_markdown(
                markdown,
                entity_type=args.entity,
                setting=args.setting,
                output_path=args.out,
            )
            print(destination)
            return 0
        except Exception as exc:
            print(f"Failed to export markdown: {exc}", file=sys.stderr)
            return 1

    parser.error(f"Unsupported command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

