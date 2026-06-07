from __future__ import annotations

import argparse
import sys

from Homebrewery.datasets import list_entity_types
from Homebrewery.exports import write_markdown
from Homebrewery.services import HomebreweryMarkdownService


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Homebrewery utility CLI.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    spell_list_parser = subparsers.add_parser(
        "spell-list",
        help="Build a spell list grouped by class, ordered by level (fantasy setting).",
    )
    spell_list_parser.add_argument(
        "--source",
        default=None,
        help="Optional source override (e.g. ORIO).",
    )
    spell_list_parser.add_argument(
        "--out",
        default=None,
        help="Output path (defaults to Homebrewery/core/markdown/spell_list_fantasy.txt).",
    )

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
        choices=["fantasy", "modern"],
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

    character_options_parser = subparsers.add_parser(
        "export-character-options",
        help="Export feats and backgrounds to separate markdown files.",
    )
    character_options_parser.add_argument(
        "--setting",
        default="modern",
        choices=["fantasy", "modern"],
        help="Content setting.",
    )
    character_options_parser.add_argument(
        "--source",
        default=None,
        help="Optional source override (e.g. VSTGCC).",
    )
    character_options_parser.add_argument(
        "--out-dir",
        default="Homebrewery/core/markdown",
        help="Directory for feat_<setting>.txt and background_<setting>.txt.",
    )

    return parser


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()

    if args.command == "spell-list":
        from FiveETools.datasets import load_entities
        from Homebrewery.core.Helpers.fantasy_spells import (
            build_fantasy_spell_list_by_class,
        )
        from pathlib import Path

        try:
            spells = load_entities(
                entity_type="spell", setting="fantasy", source_code=args.source
            )
            markdown = build_fantasy_spell_list_by_class(spells)
            out = (
                Path(args.out)
                if args.out
                else Path("Homebrewery/core/markdown/spell_list_fantasy.txt")
            )
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(markdown, encoding="utf-8")
            print(out)
            return 0
        except Exception as exc:
            print(f"Failed to build spell list: {exc}", file=sys.stderr)
            return 1

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

    if args.command == "export-character-options":
        from pathlib import Path

        service = HomebreweryMarkdownService()
        out_dir = Path(args.out_dir)
        try:
            for entity_type, title in (
                ("feat", "Feats"),
                ("background", "Backgrounds"),
            ):
                markdown = service.build_markdown(
                    entity_type=entity_type,
                    setting=args.setting,
                    source_code=args.source,
                    title=title,
                )
                destination = write_markdown(
                    markdown,
                    entity_type=entity_type,
                    setting=args.setting,
                    output_path=out_dir / f"{entity_type}_{args.setting}.txt",
                )
                print(destination)
            return 0
        except Exception as exc:
            print(f"Failed to export character options: {exc}", file=sys.stderr)
            return 1

    parser.error(f"Unsupported command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
