from __future__ import annotations

import pandas as pd

from FiveETools.datasets import modern_assembly
from FiveETools.datasets import species as species_dataset


def test_species_dataset_builds_rows_from_dataframe() -> None:
    dataframe = pd.DataFrame(
        [
            {
                "Name": "Elf",
                "Source": "ORIO",
                "Ability 1": "Dexterity",
                "Score 1": 2,
                "Ability 2": "Wisdom",
                "Score 2": 1,
                "Size ABRV": "M",
                "Walk Speed": 30,
                "Age": "Long-lived",
                "Size": "Medium",
                "Speed": "30 ft.",
                "Vision": "Darkvision",
                "Intro": "Intro text",
                "Life in Orimond": "Life text",
            },
            {
                "Name": None,
                "Source": "ORIO",
                "Intro": "Ignored",
                "Life in Orimond": "Ignored",
            },
        ]
    )

    species = species_dataset.build_species_list(
        setting="fantasy", df_species=dataframe
    )

    assert [entry["name"] for entry in species] == ["Elf"]


def test_modern_feature_assembly_filters_and_deduplicates(monkeypatch) -> None:
    dataframe = pd.DataFrame(
        [
            {
                "Name": "Fighting Style",
                "Parent": None,
                "Source": "VSTGCC",
                "Subclass": None,
                "Class": "fighter",
                "Level": 1,
                "Entry": "Choose a style.",
            },
            {
                "Name": "Fighting Style",
                "Parent": None,
                "Source": "VSTGCC",
                "Subclass": None,
                "Class": "fighter",
                "Level": 1,
                "Entry": "Choose a style.",
            },
            {
                "Name": "Arcane Tradition",
                "Parent": None,
                "Source": "VSTGCC",
                "Subclass": "Evoker",
                "Class": "wizard",
                "Level": 2,
                "Entry": "Subclass feature.",
            },
        ]
    )
    monkeypatch.setattr(
        modern_assembly.source_catalog,
        "resolve_source_context",
        lambda source_code: (source_code, source_code),
    )

    features = modern_assembly.build_features_list(
        source_code="VSTGCC",
        df_class_features=dataframe,
    )

    assert len(features) == 1
    assert features[0]["name"] == "Fighting Style"
