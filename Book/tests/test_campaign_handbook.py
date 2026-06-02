from __future__ import annotations

from typing import Any

from Book.core.Helpers.book_api import BookAPI
from Book.core.Helpers.google_docs_client import GoogleDocsClient
from Book.core.Helpers.styles import BODY_FONT, HEADING_1_COLOR, HEADING_1_FONT
from Book.core.writers import CampaignHandbookWriter
from Book.exports import get_writer_class


class _FakeGoogleDocsClient(GoogleDocsClient):
    def __init__(self) -> None:
        self.clear_called = False
        self.layout_called = False
        self.chunks: list[list[dict[str, Any]]] = []

    def clear_document(self) -> None:
        self.clear_called = True

    def batch_update_in_chunks(
        self,
        requests: list[dict[str, Any]],
        *,
        chunk_size: int = 50,
        pause_seconds: float = 0.35,
    ) -> None:
        for start in range(0, len(requests), chunk_size):
            self.chunks.append(requests[start : start + chunk_size])

    def apply_two_column_layout(self) -> None:
        self.layout_called = True


class _FakeBookAPI:
    def __init__(self, datasets: dict[str, list[dict[str, Any]]]) -> None:
        self.datasets = datasets

    def load_entities(self, entity_type: str, source: str = "fantasy") -> list[dict[str, Any]]:
        if entity_type not in self.datasets:
            raise ValueError(f"unsupported {entity_type} for {source}")
        return self.datasets[entity_type]


def test_writer_registry_exposes_full_handbook_alias() -> None:
    assert get_writer_class("campaign_handbook") is CampaignHandbookWriter
    assert get_writer_class("full_handbook") is CampaignHandbookWriter


def test_campaign_handbook_writer_includes_outline_and_sourced_sections() -> None:
    book_api = _FakeBookAPI(
        {
            "species": [
                {
                    "name": "Dwarf",
                    "alias": ["Stoneborn"],
                    "slogan": "Steady in the Deep",
                    "quote": "The mountain keeps its own counsel.",
                    "ability": [{"con": 2}],
                    "size": ["M"],
                    "speed": 25,
                    "entries": [
                        "Dwarf Traits",
                        {"type": "entries", "name": "Age", "entries": ["Adults at 50."]},
                        {"type": "entries", "name": "Darkvision", "entries": ["You can see in dim light within 60 feet."]},
                    ],
                    "fluff": {
                        "entries": [
                            {"type": "entries", "name": "Intro", "entries": ["Stoneborn and steady."]},
                            {"type": "entries", "name": "Naming Conventions", "entries": ["Clan names are earned, then inherited."]},
                        ]
                    },
                }
            ],
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
                }
            ],
            "language": [{"name": "Common", "entries": ["The trade tongue."]}],
            "monster": [
                {
                    "name": "Goblin",
                    "size": ["S"],
                    "type": "humanoid",
                    "alignment": ["N", "E"],
                    "ac": [15],
                    "hp": {"average": 7, "formula": "2d6"},
                    "speed": {"walk": 30},
                    "str": 8,
                    "dex": 14,
                    "con": 10,
                    "int": 10,
                    "wis": 8,
                    "cha": 8,
                    "cr": "1/4",
                }
            ],
            "magicitem": [{"name": "Sunblade", "entries": ["A radiant blade."]}],
            "disease": [{"name": "Ash Rot", "entries": ["A wasting sickness."]}],
        }
    )

    writer = CampaignHandbookWriter(book_api, source="fantasy")
    lines = writer.build_document_lines()

    assert "# Front Matter" in lines
    assert "# Part II. Character Creation" in lines
    assert "## Chapter 10. Species" in lines
    assert "### 10.1 Species Overview" in lines
    assert "### 10.2 Species Entries" in lines
    assert "## Dwarf" in lines
    assert "*Stoneborn - Steady in the Deep*" in lines
    assert "### 10.6 Species Tables" in lines
    assert "**Dwarf** | Ability: CON +2 | Size: Medium | Speed: 25 ft." in lines
    assert "### 19.4 Spell Lists" in lines
    assert "#### Fireball" in lines
    assert "## Appendix F. Conditions Reference" in lines


def test_campaign_handbook_writer_includes_timeline_sections_when_available() -> None:
    class _TimelineWriter(CampaignHandbookWriter):
        def _timeline_catalog(self) -> dict[str, Any] | None:
            return {
                "calendar_months": [
                    {
                        "month_order": "1st Month",
                        "month_name": "Firstcold",
                        "description": "Deep winter.",
                        "chore_name": "The Smith's Dawn",
                        "chore_description": "Forging tools.",
                        "deity_name": "Heraclus",
                        "domain": "War, Courage, Fraternity",
                    }
                ],
                "naming_groups": [
                    {"label": "A (Modifier)", "values": ["Hush", "Gaunt"]},
                    {"label": "Hours", "values": ["False dawn", "First light"]},
                ],
                "naming_template": "Year of the {A (Modifier)}",
                "weekdays": ["Avenoir", "Exulansis"],
                "holidays": [
                    {"name": "Equinox", "month_name": "FIRSTCOLD", "day": 6, "weekday": "Avenoir", "notes": None}
                ],
                "era_events": [
                    {"year": 12300, "era": "Century of Embers", "event": "The ash crowns were kindled."}
                ],
                "era_periods": [
                    {
                        "era": "Century of Embers",
                        "label": "Year of the Hush Winds / Century of Embers",
                        "start_year": 12300,
                        "end_year": 12399,
                    }
                ],
                "conflicts": [
                    {
                        "year": 12518,
                        "event": "Late Varnhallan cohesion frays.",
                        "strategic_consequence": "Competing claims harden.",
                    }
                ],
            }

    writer = _TimelineWriter(_FakeBookAPI({"species": [], "spell": [], "language": [], "monster": [], "magicitem": [], "disease": []}), source="fantasy")
    lines = writer.build_document_lines()

    assert "### 2.3 Major Eras" in lines
    assert "**Century of Embers**" in lines
    assert "### 2.4 Defining Events" in lines
    assert any("Competing claims harden." in line for line in lines)
    assert "### 8.2 Naming Conventions" in lines
    assert "Template: `Year of the {A (Modifier)}`" in lines
    assert "### 28.2 Months and Seasons" in lines
    assert "**1st Month Firstcold**" in lines
    assert "### 28.3 Festivals and Holy Days" in lines
    assert "- Equinox (FIRSTCOLD, day 6, Avenoir)" in lines


def test_generate_book_writes_in_multiple_chunks_for_large_documents() -> None:
    gdocs = _FakeGoogleDocsClient()
    book_api = BookAPI(google_docs_client=gdocs, gsheets_client=object())

    class _LargeWriter:
        source = "fantasy"

        def build_document_lines(self) -> list[str]:
            lines = ["# Large Test Document", ""]
            for index in range(700):
                lines.append(f"Paragraph {index}")
            return lines

    book_api.generate_book(_LargeWriter())

    assert gdocs.clear_called is True
    assert gdocs.layout_called is True
    assert len(gdocs.chunks) >= 2


def test_heading_bands_switch_between_single_and_two_column_sections() -> None:
    gdocs = _FakeGoogleDocsClient()
    book_api = BookAPI(google_docs_client=gdocs, gsheets_client=object())

    requests, _ = book_api._build_requests_for_lines(
        [
            "# Part I. The World of Orimond",
            "",
            "Intro paragraph.",
            "## Chapter 1. Setting Overview",
            "",
            "### 1.1 The World at a Glance",
            "",
            "Body text.",
        ],
        index=1,
    )

    section_break_count = sum(1 for request in requests if "insertSectionBreak" in request)
    section_style_columns = [
        len(request["updateSectionStyle"]["sectionStyle"]["columnProperties"])
        for request in requests
        if "updateSectionStyle" in request
    ]

    assert section_break_count >= 5
    assert section_style_columns[:6] == [1, 2, 1, 2, 1, 2]


def test_mixed_heading_sequence_returns_to_two_columns_before_h4() -> None:
    gdocs = _FakeGoogleDocsClient()
    book_api = BookAPI(google_docs_client=gdocs, gsheets_client=object())

    requests, _ = book_api._build_requests_for_lines(
        [
            "## Chapter 7. Culture and Society",
            "",
            "### 7.2 Customs and Etiquette",
            "Body paragraph.",
            "#### Formal Address",
            "Follow-up paragraph.",
        ],
        index=1,
    )

    section_style_columns = [
        len(request["updateSectionStyle"]["sectionStyle"]["columnProperties"])
        for request in requests
        if "updateSectionStyle" in request
    ]

    assert section_style_columns[:4] == [1, 2, 1, 2]
    assert all(columns == 2 for columns in section_style_columns[3:])


def test_google_docs_style_helpers_emit_phb_lite_payloads() -> None:
    client = GoogleDocsClient.__new__(GoogleDocsClient)

    heading_requests = client.create_heading_style_requests(
        start_index=1,
        end_index=18,
        level=1,
    )
    body_requests = client.create_body_style_requests(
        start_index=20,
        end_index=30,
    )
    section_request = client.create_section_style_request(
        start_index=1,
        end_index=10,
        columns=2,
    )

    heading_paragraph = heading_requests[0]["updateParagraphStyle"]["paragraphStyle"]
    heading_text = heading_requests[1]["updateTextStyle"]["textStyle"]
    body_paragraph = body_requests[0]["updateParagraphStyle"]["paragraphStyle"]
    body_text = body_requests[1]["updateTextStyle"]["textStyle"]
    section_style = section_request["updateSectionStyle"]["sectionStyle"]

    assert heading_paragraph["alignment"] == "CENTER"
    assert heading_paragraph["keepWithNext"] is True
    assert heading_text["weightedFontFamily"]["fontFamily"] == HEADING_1_FONT
    assert heading_text["foregroundColor"]["color"]["rgbColor"] == HEADING_1_COLOR
    assert heading_text["bold"] is True
    assert body_paragraph["alignment"] == "JUSTIFIED"
    assert body_text["weightedFontFamily"]["fontFamily"] == BODY_FONT
    assert section_style["columnSeparatorStyle"] == "NONE"
    assert len(section_style["columnProperties"]) == 2


def test_google_docs_one_column_style_uses_concrete_column_properties() -> None:
    client = GoogleDocsClient.__new__(GoogleDocsClient)

    request = client.create_section_style_request(
        start_index=1,
        end_index=10,
        columns=1,
    )

    section_style = request["updateSectionStyle"]["sectionStyle"]
    assert section_style["columnProperties"]
    assert section_style["columnSeparatorStyle"] == "NONE"
