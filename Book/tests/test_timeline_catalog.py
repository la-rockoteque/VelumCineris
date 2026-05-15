from __future__ import annotations

from Book.datasets.timeline_catalog import _derive_naming_template, _merge_holidays, _parse_conflicts


def test_derive_naming_template_uses_group_labels() -> None:
    template = _derive_naming_template(
        [
            {"label": "A (Modifier)"},
            {"label": "A (Phenomenon)"},
            {"label": "A (Anchor)"},
            {"label": "A (Modifier) (2)"},
        ]
    )

    assert template == "Year of the {A (Modifier)} {A (Phenomenon)} Century of the {A (Anchor)} {A (Modifier)}"


def test_merge_holidays_deduplicates_present_and_sheet_sources() -> None:
    merged = _merge_holidays(
        [
            {"name": "Equinox", "month_name": "FIRSTCOLD", "day": 6, "source": "holidays"},
        ],
        [
            {"name": "Equinox", "month_name": "FIRSTCOLD", "day": 6, "source": "present"},
            {"name": "Solstice", "month_name": "LEAFWANE", "day": None, "source": "present"},
        ],
    )

    assert len(merged) == 2
    assert merged[0]["name"] == "Equinox"
    assert merged[1]["name"] == "Solstice"


def test_parse_conflicts_reads_year_event_and_consequence() -> None:
    conflicts = _parse_conflicts(
        [
            ["Year", "Event", "Strategic consequence"],
            [12518, "Late Varnhallan cohesion frays.", "Competing claims harden."],
        ]
    )

    assert conflicts == [
        {
            "row_number": 2,
            "year": 12518,
            "event": "Late Varnhallan cohesion frays.",
            "strategic_consequence": "Competing claims harden.",
        }
    ]
