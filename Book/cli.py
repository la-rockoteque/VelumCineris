from __future__ import annotations

import argparse
import sys
from pathlib import Path

if __package__ in (None, ""):
    REPO_ROOT = Path(__file__).resolve().parents[1]
    if str(REPO_ROOT) not in sys.path:
        sys.path.insert(0, str(REPO_ROOT))

from Book.datasets import list_sources
from Book.core.entities import list_entity_types
from Book.exports import list_book_types
from Book.services import BookGenerationService


def _add_module_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--entity-type",
        required=True,
        choices=list_entity_types(),
        help="Entity module to generate.",
    )
    parser.add_argument(
        "--source",
        choices=list_sources(),
        default="fantasy",
        help="Content source setting.",
    )
    parser.add_argument(
        "--title",
        help="Optional module title. Defaults to a title-cased entity type.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        help="Optional maximum number of entities to include.",
    )


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Book generation utility CLI.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    preview_parser = subparsers.add_parser(
        "preview",
        help="Preview formatter output in terminal.",
    )
    preview_parser.add_argument("--entity", required=True, help="Entity type to preview.")
    preview_parser.add_argument(
        "--source",
        choices=list_sources(),
        default="fantasy",
        help="Content source setting.",
    )
    preview_parser.add_argument(
        "--limit",
        type=int,
        default=5,
        help="Number of entities to preview.",
    )

    generate_parser = subparsers.add_parser(
        "generate",
        help="Generate a Google Docs book.",
    )
    generate_parser.add_argument("--doc-id", required=True, help="Google Docs document ID.")
    generate_parser.add_argument(
        "--book-type",
        required=True,
        choices=list_book_types(),
        help="Writer profile to use.",
    )
    generate_parser.add_argument(
        "--source",
        choices=list_sources(),
        default="fantasy",
        help="Content source setting.",
    )
    generate_parser.add_argument(
        "--credentials",
        default="FiveETools/key.json",
        help="Service-account credentials path.",
    )

    homebrewery_parser = subparsers.add_parser(
        "export-homebrewery",
        help="Export a complete book as Homebrewery markdown.",
    )
    homebrewery_parser.add_argument(
        "--book-type",
        required=True,
        choices=list_book_types(),
        help="Writer profile to use.",
    )
    homebrewery_parser.add_argument(
        "--source",
        choices=list_sources(),
        default="fantasy",
        help="Content source setting.",
    )
    homebrewery_parser.add_argument(
        "--output",
        required=True,
        help="Path for the generated Homebrewery markdown file.",
    )

    markdown_parser = subparsers.add_parser(
        "export-markdown",
        help="Export a complete book as canonical markdown.",
    )
    markdown_parser.add_argument(
        "--book-type",
        required=True,
        choices=list_book_types(),
        help="Writer profile to use.",
    )
    markdown_parser.add_argument(
        "--source",
        choices=list_sources(),
        default="fantasy",
        help="Content source setting.",
    )
    markdown_parser.add_argument(
        "--output",
        required=True,
        help="Path for the generated canonical markdown file.",
    )

    generate_module_parser = subparsers.add_parser(
        "generate-module",
        help="Generate a standalone entity module in Google Docs.",
    )
    _add_module_arguments(generate_module_parser)
    generate_module_parser.add_argument(
        "--doc-id",
        required=True,
        help="Google Docs document ID.",
    )
    generate_module_parser.add_argument(
        "--credentials",
        default="FiveETools/key.json",
        help="Service-account credentials path.",
    )

    module_markdown_parser = subparsers.add_parser(
        "export-module-markdown",
        help="Export a standalone entity module as canonical markdown.",
    )
    _add_module_arguments(module_markdown_parser)
    module_markdown_parser.add_argument(
        "--output",
        required=True,
        help="Path for the generated canonical markdown file.",
    )

    module_homebrewery_parser = subparsers.add_parser(
        "export-module-homebrewery",
        help="Export a standalone entity module as Homebrewery markdown.",
    )
    _add_module_arguments(module_homebrewery_parser)
    module_homebrewery_parser.add_argument(
        "--output",
        required=True,
        help="Path for the generated Homebrewery markdown file.",
    )

    return parser


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()
    service = BookGenerationService()

    if args.command == "preview":
        service.preview_section(
            entity_type=args.entity,
            source=args.source,
            limit=args.limit,
        )
        return 0

    if args.command == "generate":
        service.generate_book(
            book_type=args.book_type,
            doc_id=args.doc_id,
            source=args.source,
            credentials_path=args.credentials,
        )
        print(f"https://docs.google.com/document/d/{args.doc_id}/edit")
        return 0

    if args.command == "export-homebrewery":
        path = service.export_homebrewery(
            book_type=args.book_type,
            source=args.source,
            output_path=args.output,
        )
        print(path)
        return 0

    if args.command == "export-markdown":
        path = service.export_markdown(
            book_type=args.book_type,
            source=args.source,
            output_path=args.output,
        )
        print(path)
        return 0

    if args.command == "generate-module":
        service.generate_module(
            entity_type=args.entity_type,
            doc_id=args.doc_id,
            source=args.source,
            title=args.title,
            limit=args.limit,
            credentials_path=args.credentials,
        )
        print(f"https://docs.google.com/document/d/{args.doc_id}/edit")
        return 0

    if args.command == "export-module-markdown":
        path = service.export_module_markdown(
            entity_type=args.entity_type,
            source=args.source,
            title=args.title,
            limit=args.limit,
            output_path=args.output,
        )
        print(path)
        return 0

    if args.command == "export-module-homebrewery":
        path = service.export_module_homebrewery(
            entity_type=args.entity_type,
            source=args.source,
            title=args.title,
            limit=args.limit,
            output_path=args.output,
        )
        print(path)
        return 0

    parser.error(f"Unsupported command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
