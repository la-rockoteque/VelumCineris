from __future__ import annotations

from typing import Any, Callable

from Book.core.Helpers.book_api import BookAPI
from Book.core.Helpers.google_docs_client import GoogleDocsClient
from Book.core.entities import list_entity_types, render_entity_markdown
from Book.core.markdown import PAGE_BREAK_MARKER
from Book.core.renderers import HomebreweryRenderer
from Book.core.writers.divine_codex import DivineCodexWriter
from Book.core.writers.base import BaseWriter
from Book.services import BookGenerationService


class _FakeGoogleDocsClient(GoogleDocsClient):
    def __init__(self) -> None:
        pass


class _FakeBookAPI:
    def __init__(self) -> None:
        self.datasets = {
            "spell": [
                {
                    "name": "Fireball",
                    "level": 3,
                    "school": "V",
                    "time": [{"number": 1, "unit": "action"}],
                    "range": {"type": "point", "distance": {"type": "feet", "amount": 150}},
                    "components": {"v": True, "s": True},
                    "duration": [{"type": "instant"}],
                    "entries": ["A burst of fire."],
                },
                {
                    "name": "Light",
                    "level": 0,
                    "school": "V",
                    "entries": ["An object sheds bright light."],
                },
            ]
        }

    def load_entities(self, entity_type: str, source: str = "fantasy") -> list[dict[str, Any]]:
        return self.datasets[entity_type]


class _FakeWriter:
    def __init__(self, book_api: Any, source: str = "fantasy") -> None:
        self.book_api = book_api
        self.source = source

    def build_markdown(self) -> str:
        return "# Test Book\n\nBody from markdown.\n"


class _CoverWriter(BaseWriter):
    def get_sections(self) -> list[tuple[str, str, Callable | None]]:
        return []

    def get_book_title(self) -> str:
        return "Orimond Player Guide"


def test_service_renders_and_exports_canonical_markdown(tmp_path, monkeypatch) -> None:
    service = BookGenerationService()
    monkeypatch.setattr(service, "create_book_api", lambda *, source: _FakeBookAPI())
    monkeypatch.setattr(
        "Book.services.generation_service.get_writer_class",
        lambda book_type: _FakeWriter,
    )

    assert service.render_markdown(book_type="campaign_handbook") == (
        "# Test Book\n\nBody from markdown.\n"
    )

    output_path = tmp_path / "book.md"
    result = service.export_markdown(
        book_type="campaign_handbook",
        output_path=output_path,
    )

    assert result == output_path
    assert output_path.read_text(encoding="utf-8") == "# Test Book\n\nBody from markdown.\n"


def test_book_cover_uses_homebrewery_front_cover_markup() -> None:
    writer = _CoverWriter(book_api=object(), source="fantasy")
    rendered = writer.write_cover_page()

    assert rendered.startswith("{{frontCover}}\n")
    assert "{{logo ![](https://homebrewery.naturalcrit.com/assets/naturalCritLogoRed.svg)}}" in rendered
    assert "# Orimond" in rendered
    assert "## Player Guide" in rendered
    assert "{{banner HOMEBREW}}" in rendered
    assert "{{footnote\n  A Homebrew Compendium · D&D 5th Edition\n}}" in rendered
    assert "![Cover Image](" in rendered
    assert "{position:absolute,top:0,right:0px,height:100%}" in rendered
    assert PAGE_BREAK_MARKER in rendered
    assert "COVER_TITLE" not in rendered


def test_section_cover_page_uses_homebrewery_chapter_opener() -> None:
    writer = _CoverWriter(book_api=object(), source="fantasy")
    rendered = writer.write_section_cover_page("Races", 1)

    assert rendered == (
        "# Chapter I\n\n"
        "## Races\n\n"
        "{{imageMaskEdge8,--offset:10cm,--rotation:180\n"
        "  ![Chapter I Cover](https://homebrewery.naturalcrit.com/assets/frigate.webp)"
        "{position:absolute,bottom:0,right:0,height:100%}\n"
        "}}\n\n"
        "{{pageNumber,auto}}\n"
        f"{PAGE_BREAK_MARKER}\n"
    )


def test_service_renders_and_exports_standalone_module(tmp_path, monkeypatch) -> None:
    service = BookGenerationService()
    monkeypatch.setattr(service, "create_book_api", lambda *, source: _FakeBookAPI())

    markdown = service.render_module_markdown(
        entity_type="spell",
        source="fantasy",
        title="Starter Spells",
        limit=1,
    )

    assert markdown.startswith("# Starter Spells\n")
    assert "#### Fireball" in markdown
    assert "#### Light" not in markdown
    assert "COVER_TITLE" not in markdown
    assert "Table of Contents" not in markdown

    markdown_path = service.export_module_markdown(
        entity_type="spell",
        output_path=tmp_path / "starter-spells.md",
        title="Starter Spells",
        limit=1,
    )
    homebrewery_path = service.export_module_homebrewery(
        entity_type="spell",
        output_path=tmp_path / "starter-spells.homebrewery.md",
        title="Starter Spells",
        limit=1,
    )

    assert markdown_path.read_text(encoding="utf-8") == markdown
    assert "\\page" in homebrewery_path.read_text(encoding="utf-8")


def test_service_renders_deities_only_module(monkeypatch) -> None:
    service = BookGenerationService()
    book_api = _FakeBookAPI()
    book_api.datasets["deity"] = [
        {
            "name": "Heraclus",
            "epithet": "The First Flame",
            "pantheon": "The Old Gods",
            "domains": ["Light", "Life"],
            "alignment": "Lawful Good",
            "description": "Heraclus guards the dawn.",
            "lore": "The first temples faced east.",
        }
    ]
    monkeypatch.setattr(service, "create_book_api", lambda *, source: book_api)

    markdown = service.render_module_markdown(entity_type="deity", title="Deities")

    assert markdown.startswith("# Deities\n")
    assert "## Heraclus\n##### *The First Flame*" in markdown
    assert (
        "{{imageMaskEdge5,--offset:5%,--rotation:90\n"
        "![Heraclus](https://raw.githubusercontent.com/la-rockoteque/Vestigium/"
        "refs/heads/main/assets/art/Dieties/Heraclus.png)"
        "{position:absolute,top:0,left:-20%,height:100%}\n}}"
    ) in markdown
    assert "| **Domains** | Light, Life |" in markdown
    assert "### Stories and Lore" not in markdown
    assert "The first temples faced east." not in markdown


def test_deity_markdown_resolves_existing_art_filename_aliases() -> None:
    markdown = render_entity_markdown(
        "deity",
        {
            "name": "The Legislator",
            "epithet": "Pillar of Stability",
            "_image_side": "left",
        },
    )

    assert (
        "{{imageMaskEdge5,--offset:5%,--rotation:90\n"
        "![The Legislator](https://raw.githubusercontent.com/la-rockoteque/Vestigium/"
        "refs/heads/main/assets/art/Dieties/Legislator.png)"
        "{position:absolute,top:0,left:-20%,height:100%}\n}}"
    ) in markdown


def test_divine_codex_sorts_deities_and_builds_appendices() -> None:
    class _DeityBookAPI:
        def load_entities(self, entity_type: str, source: str) -> list[dict[str, Any]]:
            assert entity_type == "deity"
            return [
                {
                    "name": "Zars",
                    "alignment": "Chaotic-Good",
                    "domains": ["War", "Glory"],
                    "pantheon": "Children",
                },
                {
                    "name": "Artémiz",
                    "alignment": "Lawful Good",
                    "domains": ["Hunt; Nature"],
                    "pantheon": "Old Gods",
                },
                {
                    "name": "Omnis",
                    "alignment": "Neutral",
                },
            ]

    writer = DivineCodexWriter(book_api=_DeityBookAPI())
    markdown = writer.build_markdown()

    assert writer.get_sections() == [("Deities", "deity", None)]
    assert "deity" in list_entity_types()
    assert markdown.index("## Artémiz") < markdown.index("## Omnis") < markdown.index("## Zars")
    assert "{{frontCover}}" in markdown
    assert "# Divine Codex\n## Dieties, worships and rituals" in markdown
    assert "{{insideCover}}" in markdown
    assert "{{toc,wide" in markdown
    assert "<!-- PAGE_BREAK -->" not in markdown
    assert "\\page" in markdown
    assert "# APPENDIX D\n## Deities by domain" in markdown
    assert "### Hunt\n\n- Artémiz" in markdown
    assert "### Nature\n\n- Artémiz" in markdown
    assert "### Unspecified\n\n- Omnis" in markdown
    assert "# APPENDIX E\n## Deities by alignment" in markdown
    assert "### Lawful\n\n#### Good\n\n- Artémiz" in markdown
    assert "\\column\n\n### Neutral\n\n#### Neutral\n\n- Omnis" in markdown
    assert "# APPENDIX F\n## Deities by pantheon" in markdown
    assert "### Children\n\n- Zars" in markdown
    assert not markdown.rstrip().endswith("\\page")
    assert "\\page\n\n## Omnis" in markdown


def test_divine_codex_paginates_long_deity_blocks() -> None:
    writer = DivineCodexWriter(book_api=object())
    markdown, used_height = writer._paginate_markdown(
        "\n\n".join(
            [
                "## First Deity\n##### *First Epithet*",
                "{{imageMaskEdge3,--offset:5%,--rotation:270\n"
                "![First](https://example.com/first.png)"
                "{position:absolute,top:0,right:-20%,height:100%}\n}}",
                "A" * 1200,
                "## Second Deity",
                "{{imageMaskEdge5,--offset:5%,--rotation:90\n"
                "![Second](https://example.com/second.png)"
                "{position:absolute,top:0,left:-20%,height:100%}\n}}",
            ]
        ),
        used_height=50,
    )

    assert markdown.count("\\page") >= 1
    assert "<!-- PAGE_BREAK -->" not in markdown
    assert used_height < 1320


def test_homebrewery_renderer_uses_page_break_marker() -> None:
    rendered = HomebreweryRenderer().render_markdown(
        f"# Test\n\nBefore.\n\n{PAGE_BREAK_MARKER}\n\nAfter.\n"
    )

    assert rendered == "# Test\n\nBefore.\n\n\\page\n\nAfter.\n"


def test_species_markdown_uses_two_page_homebrewery_layout() -> None:
    rendered = render_entity_markdown(
        "species",
        {
            "name": "Aestari",
            "alias": ["Scions of Clarity, Children of the Threshold"],
            "slogan": "The Many Faces of Power",
            "quote": "Perfection is not a state.",
            "fluff": {
                "entries": [
                    {"name": "Intro", "entries": ["Intro text."]},
                    {"name": "Origin", "entries": ["Origin text."]},
                    {"name": "Appearance", "entries": ["Appearance text."]},
                    {"name": "Culture & Identity", "entries": ["Culture text."]},
                    {"name": "Societal Roles", "entries": ["Roles text."]},
                ]
            },
            "ability": [{"int": 2}, {"dex": 1}],
            "entries": [
                "Aestari Traits",
                {"name": "Age", "entries": ["Adults around 100."]},
                {"name": "Speed", "entries": ["Your base walking speed is 30ft"]},
            ],
        },
    )

    assert rendered.startswith("{{imageMaskEdge1,--offset:2%,--rotation:90")
    assert "![Male Aestari]" in rendered
    assert "\\column" in rendered
    assert "*Scions of Clarity, Children of the Threshold - The Many Faces of Power*" in rendered
    assert "#### Culture & Identity\n___" in rendered
    assert "#### Societal Roles\n___" in rendered
    assert "#### Aestari Traits\n___" in rendered
    assert rendered.count("{{pageNumber,auto}}") == 2
    assert rendered.count(PAGE_BREAK_MARKER) == 2
    assert "**Ability Score Increase.** Your Intelligence score increases by 2" in rendered


def test_google_docs_markdown_renderer_handles_core_blocks() -> None:
    gdocs = _FakeGoogleDocsClient()
    book_api = BookAPI(google_docs_client=gdocs, gsheets_client=object())

    requests, _ = book_api._build_requests_for_markdown(
        "\n".join(
            [
                "COVER_TITLE: Orimond",
                "",
                PAGE_BREAK_MARKER,
                "",
                "# Part I",
                "",
                "Body with **bold**, *italic*, and `code`.",
                "",
                "- First item",
                "- Second item",
                "",
                "| Name | Value |",
                "| --- | --- |",
                "| One | Two |",
                "",
            ]
        ),
        index=1,
    )

    inserted_text = "".join(
        request["insertText"]["text"]
        for request in requests
        if "insertText" in request
    )

    assert "Orimond" in inserted_text
    assert "Part I" in inserted_text
    assert "Body with bold, italic, and code." in inserted_text
    assert "- First item\n- Second item\n" in inserted_text
    assert "Name | Value" in inserted_text
    assert any("insertPageBreak" in request for request in requests)
    assert any(
        request.get("updateTextStyle", {}).get("textStyle", {}).get("bold") is True
        for request in requests
    )
    assert any(
        request.get("updateTextStyle", {}).get("textStyle", {}).get("italic") is True
        for request in requests
    )
