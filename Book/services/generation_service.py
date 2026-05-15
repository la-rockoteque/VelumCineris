from __future__ import annotations

from typing import Any, cast
from pathlib import Path

from Book.core.Helpers.book_api import BookAPI
from Book.core.renderers import HomebreweryRenderer
from Book.datasets import get_sheets_client, normalize_source
from Book.exports import get_writer_class


class BookGenerationService:
    def create_book_api(
        self,
        *,
        source: str,
        doc_id: str | None = None,
        credentials_path: str = "FiveETools/key.json",
    ) -> BookAPI:
        normalized_source = normalize_source(source)
        sheets_client = get_sheets_client(normalized_source)

        if doc_id is None:
            # Preview operations do not require Google Docs writes.
            return BookAPI(
                google_docs_client=cast(Any, object()),
                gsheets_client=sheets_client,
            )

        from Book.core.Helpers.google_docs_client import GoogleDocsClient

        gdocs_client = GoogleDocsClient(doc_id, credentials_path)
        return BookAPI(google_docs_client=gdocs_client, gsheets_client=sheets_client)

    def preview_section(
        self,
        *,
        entity_type: str,
        source: str = "fantasy",
        limit: int = 5,
    ) -> None:
        normalized_source = normalize_source(source)
        book_api = self.create_book_api(source=normalized_source)
        book_api.preview_section(
            entity_type=entity_type,
            source=normalized_source,
            limit=limit,
        )

    def generate_book(
        self,
        *,
        book_type: str,
        doc_id: str,
        source: str = "fantasy",
        credentials_path: str = "FiveETools/key.json",
    ) -> Any:
        normalized_source = normalize_source(source)
        book_api = self.create_book_api(
            source=normalized_source,
            doc_id=doc_id,
            credentials_path=credentials_path,
        )
        writer_class = get_writer_class(book_type)
        writer = writer_class(book_api, source=normalized_source)
        return book_api.generate_book(writer, doc_id=doc_id)

    def export_homebrewery(
        self,
        *,
        book_type: str,
        output_path: str | Path,
        source: str = "fantasy",
    ) -> Path:
        normalized_source = normalize_source(source)
        book_api = self.create_book_api(source=normalized_source)
        writer_class = get_writer_class(book_type)
        writer = writer_class(book_api, source=normalized_source)

        lines = writer.build_document_lines()
        rendered = HomebreweryRenderer().render(lines)

        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(rendered, encoding="utf-8")
        return path
