"""
Tests for entity formatters.
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from Book.core.formatters import (
    SpellFormatter,
    SpeciesFormatter,
    MonsterFormatter,
    BackgroundFormatter,
    FeatFormatter,
)


def test_spell_formatter():
    """Test SpellFormatter with sample spell."""
    formatter = SpellFormatter()

    # Sample spell in 5etools format
    spell = {
        "name": "Fireball",
        "level": 3,
        "school": "V",
        "time": [{"number": 1, "unit": "action"}],
        "range": {"type": "point", "distance": {"type": "feet", "amount": 150}},
        "components": {"v": True, "s": True, "m": "a tiny ball of bat guano and sulfur"},
        "duration": [{"type": "instant"}],
        "entries": [
            "A bright streak flashes from your pointing finger to a point you choose within range and then blossoms with a low roar into an explosion of flame."
        ],
    }

    lines = formatter.format_entity(spell)

    # Verify output
    assert len(lines) > 0
    assert any("Fireball" in line for line in lines)
    assert any("3rd-level Evocation" in line for line in lines)
    print(f"✓ SpellFormatter test passed ({len(lines)} lines)")


def test_species_formatter():
    """Test SpeciesFormatter with sample species."""
    formatter = SpeciesFormatter()

    # Sample species in 5etools format
    species = {
        "name": "Dwarf",
        "size": "M",
        "speed": {"walk": 25},
        "ability": [{"con": 2}],
        "entries": ["Bold and hardy, dwarves are known as skilled warriors."],
        "trait": [
            {
                "name": "Darkvision",
                "entries": ["You can see in dim light within 60 feet."],
            }
        ],
    }

    lines = formatter.format_entity(species)

    # Verify output
    assert len(lines) > 0
    assert any("Dwarf" in line for line in lines)
    print(f"✓ SpeciesFormatter test passed ({len(lines)} lines)")


def test_monster_formatter():
    """Test MonsterFormatter with sample monster."""
    formatter = MonsterFormatter()

    # Sample monster in 5etools format
    monster = {
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
        "trait": [
            {
                "name": "Nimble Escape",
                "entries": ["The goblin can take the Disengage or Hide action as a bonus action."],
            }
        ],
    }

    lines = formatter.format_entity(monster)

    # Verify output
    assert len(lines) > 0
    assert any("Goblin" in line for line in lines)
    print(f"✓ MonsterFormatter test passed ({len(lines)} lines)")


def test_background_formatter():
    """Test BackgroundFormatter with sample background."""
    formatter = BackgroundFormatter()

    # Sample background in 5etools format
    background = {
        "name": "Acolyte",
        "entries": ["You have spent your life in service to a temple."],
        "feature": [
            {
                "name": "Shelter of the Faithful",
                "entries": ["You can perform religious ceremonies."],
            }
        ],
    }

    lines = formatter.format_entity(background)

    # Verify output
    assert len(lines) > 0
    assert any("Acolyte" in line for line in lines)
    print(f"✓ BackgroundFormatter test passed ({len(lines)} lines)")


def test_feat_formatter():
    """Test FeatFormatter with sample feat."""
    formatter = FeatFormatter()

    # Sample feat in 5etools format
    feat = {
        "name": "Alert",
        "entries": [
            "You gain a +5 bonus to initiative.",
            "You can't be surprised while you are conscious.",
        ],
    }

    lines = formatter.format_entity(feat)

    # Verify output
    assert len(lines) > 0
    assert any("Alert" in line for line in lines)
    print(f"✓ FeatFormatter test passed ({len(lines)} lines)")


if __name__ == "__main__":
    print("Running formatter tests...\n")

    test_spell_formatter()
    test_species_formatter()
    test_monster_formatter()
    test_background_formatter()
    test_feat_formatter()

    print("\n✓ All tests passed!")
