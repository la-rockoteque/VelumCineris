from pathlib import Path

from Homebrewery import cli
from Homebrewery.datasets import list_entity_types, normalize_setting
from Homebrewery.mappers import map_entity_markdown


def test_feat_and_background_are_supported_entity_types() -> None:
    assert "feat" in list_entity_types()
    assert "background" in list_entity_types()
    assert normalize_setting("fantasy") == "fantasy"


def test_feat_markdown_is_independent_section() -> None:
    markdown = map_entity_markdown(
        "feat",
        {
            "name": "quick study",
            "entries": ["You learn rapidly.", "Gain proficiency in one skill."],
        },
    )

    assert markdown == (
        "## Quick Study\nYou learn rapidly.\nGain proficiency in one skill."
    )


def test_background_markdown_formats_proficiencies_and_feature() -> None:
    markdown = map_entity_markdown(
        "background",
        {
            "name": "Archivist",
            "entries": [
                {
                    "type": "list",
                    "items": [
                        {
                            "type": "item",
                            "name": "Skill Proficiencies",
                            "entry": "{@skill History}, {@skill Investigation}",
                        }
                    ],
                },
                {
                    "type": "entries",
                    "name": "Research Access",
                    "entries": ["You know where restricted records are kept."],
                },
            ],
        },
    )

    assert "## Archivist" in markdown
    assert "- **Skill Proficiencies:** History, Investigation" in markdown
    assert "### Research Access" in markdown


def test_character_options_command_writes_separate_files(
    monkeypatch,
    tmp_path: Path,
) -> None:
    def build_markdown(**kwargs) -> str:
        return f"# {kwargs['title']}\n\n{kwargs['entity_type']} content"

    monkeypatch.setattr(
        cli.HomebreweryMarkdownService,
        "build_markdown",
        staticmethod(build_markdown),
    )
    monkeypatch.setattr(
        "sys.argv",
        [
            "homebrewery",
            "export-character-options",
            "--out-dir",
            str(tmp_path),
        ],
    )

    assert cli.main() == 0
    assert (tmp_path / "feat_modern.txt").read_text(encoding="utf-8") == (
        "# Feats\n\nfeat content"
    )
    assert (tmp_path / "background_modern.txt").read_text(encoding="utf-8") == (
        "# Backgrounds\n\nbackground content"
    )
