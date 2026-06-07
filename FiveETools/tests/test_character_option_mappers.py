import pandas as pd

from FiveETools.mappers.background_mapper import map_background_row
from FiveETools.mappers.feat_mapper import map_feat_row


def test_map_feat_row_supports_normalized_orimond_schema() -> None:
    row = pd.Series(
        {
            "Name": "Threshold Touched",
            "Prerequisite Text": "Wisdom 13 or higher",
            "Rules Text": "You can interfere with planar movement near you.",
            "Rules Bullets": (
                "Prevent Teleport:: Negate nearby teleportation.; "
                "Threshold Sense:: Detect planar effects."
            ),
        }
    )

    feat = map_feat_row(row, json_source="ORIO")

    assert feat["name"] == "threshold touched"
    assert feat["source"] == "ORIO"
    assert feat["entries"] == [
        "*Prerequisite: Wisdom 13 or higher*",
        "You can interfere with planar movement near you.",
        "### Prevent Teleport\nNegate nearby teleportation.",
        "### Threshold Sense\nDetect planar effects.",
    ]


def test_map_background_row_supports_normalized_orimond_schema() -> None:
    row = pd.Series(
        {
            "Name": "Veil Navigator",
            "Skill Proficiency Choice": "Perception; Survival",
            "Tool Proficiency Choice": "Navigator's Tools",
            "Language Choice": "Trade Pidgin; Marillic",
            "Equipment Text": "Navigator's tools, sextant, travel clothes",
            "Feature Name": "Veilway Familiarity",
            "Feature Rules Text": "You know established safe routes through the Veil.",
            "Feature Bullets": (
                "Veil Passage:: You can find safe Veil routes.; "
                "Local Trust:: Veil guides treat you as known."
            ),
        }
    )

    background = map_background_row(row, source="ORIO", json_source="ORIO")

    assert background["name"] == "Veil Navigator"
    assert background["skillProficiencies"] == [{"perception": True, "survival": True}]
    assert background["entries"][1]["name"] == "Veilway Familiarity"
    assert background["entries"][2]["name"] == "Veil Passage"
    assert background["entries"][3]["name"] == "Local Trust"
