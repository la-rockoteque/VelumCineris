from __future__ import annotations

from typing import Any

from Book.core.renderers import HomebreweryRenderer
from Book.services import BookGenerationService


def test_homebrewery_renderer_converts_book_markers() -> None:
    rendered = HomebreweryRenderer().render(
        [
            "COVER_TAGLINE: A Homebrew Compendium · D&D 5th Edition",
            "",
            "COVER_TITLE: Orimond",
            "",
            "COVER_IMAGE: https://example.com/cover.png",
            "",
            "COVER_SUBTITLE: Orimond Campaign Handbook",
            "",
            "---",
            "",
            "# Chapter 1",
            "Body text.",
            "─" * 30,
            "",
            "| Name | Value |",
            "| --- | --- |",
            "| One | Two |",
        ]
    )

    assert "##### A Homebrew Compendium · D&D 5th Edition" in rendered
    assert "# Orimond" in rendered
    assert "![cover image](https://example.com/cover.png)" in rendered
    assert "### Orimond Campaign Handbook" in rendered
    assert "\\page" in rendered
    assert "___" in rendered
    assert "| --- | --- |" in rendered


def test_service_exports_homebrewery_from_same_writer_lines(
    tmp_path,
    monkeypatch,
) -> None:
    class _FakeBookAPI:
        pass

    class _FakeWriter:
        def __init__(self, book_api: Any, source: str = "fantasy") -> None:
            self.book_api = book_api
            self.source = source

        def build_document_lines(self) -> list[str]:
            return [
                "COVER_TITLE: Test Book",
                "",
                "---",
                "",
                "# Test Section",
                "Same writer content.",
            ]

    service = BookGenerationService()
    monkeypatch.setattr(service, "create_book_api", lambda *, source: _FakeBookAPI())
    monkeypatch.setattr(
        "Book.services.generation_service.get_writer_class",
        lambda book_type: _FakeWriter,
    )

    output_path = tmp_path / "test-book.homebrewery.md"
    result = service.export_homebrewery(
        book_type="campaign_handbook",
        source="fantasy",
        output_path=output_path,
    )

    assert result == output_path
    assert output_path.read_text(encoding="utf-8") == (
        "# Test Book\n\n\\page\n\n# Test Section\nSame writer content.\n"
    )
