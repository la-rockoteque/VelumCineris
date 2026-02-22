"""Unit tests for spell converter"""
import pytest
import sys
sys.path.insert(0, '/Users/rocko/dev/Perso/VelumCineris')

from DNDBeyond.helpers.converter import convert_spell_to_ddb


class TestSchoolMapping:
    """Test spell school ID mapping"""

    def test_evocation(self):
        spell = {"name": "Test", "school": "V", "level": 0}
        result = convert_spell_to_ddb(spell)
        assert result["school_id"] == 7, "Evocation should be ID 7"

    def test_transmutation(self):
        spell = {"name": "Test", "school": "T", "level": 0}
        result = convert_spell_to_ddb(spell)
        assert result["school_id"] == 10, "Transmutation should be ID 10"

    def test_abjuration(self):
        spell = {"name": "Test", "school": "A", "level": 0}
        result = convert_spell_to_ddb(spell)
        assert result["school_id"] == 3, "Abjuration should be ID 3"

    def test_all_schools(self):
        schools = {
            "A": 3, "C": 4, "D": 5, "E": 6,
            "V": 7, "I": 8, "N": 9, "T": 10
        }
        for letter, expected_id in schools.items():
            spell = {"name": "Test", "school": letter, "level": 0}
            result = convert_spell_to_ddb(spell)
            assert result["school_id"] == expected_id, f"School {letter} should be ID {expected_id}"


class TestRangeAndOrigin:
    """Test range and origin mapping"""

    def test_self_range(self):
        spell = {
            "name": "Test",
            "level": 0,
            "range": {"type": "point", "distance": {"type": "self"}}
        }
        result = convert_spell_to_ddb(spell)
        assert result["origin_id"] == 1, "Self should be origin ID 1"
        assert result["range"] == 0, "Self range should be 0"

    def test_touch_range(self):
        spell = {
            "name": "Test",
            "level": 0,
            "range": {"type": "point", "distance": {"type": "touch"}}
        }
        result = convert_spell_to_ddb(spell)
        assert result["origin_id"] == 2, "Touch should be origin ID 2"
        assert result["range"] == 0, "Touch range should be 0"

    def test_ranged_30_feet(self):
        spell = {
            "name": "Test",
            "level": 0,
            "range": {"type": "point", "distance": {"type": "feet", "amount": 30.0}}
        }
        result = convert_spell_to_ddb(spell)
        assert result["origin_id"] == 3, "Distance should be origin ID 3 (Ranged)"
        assert result["range"] == 30, "Range should be 30 (int, not float)"
        assert isinstance(result["range"], int), "Range must be int type"

    def test_ranged_5_feet(self):
        spell = {
            "name": "Test",
            "level": 0,
            "range": {"type": "point", "distance": {"type": "feet", "amount": 5.0}}
        }
        result = convert_spell_to_ddb(spell)
        assert result["origin_id"] == 3, "Distance should be origin ID 3 (Ranged)"
        assert result["range"] == 5, "Range should be 5 (int, not float)"

    def test_sight_range(self):
        spell = {
            "name": "Test",
            "level": 0,
            "range": {"type": "point", "distance": {"type": "sight"}}
        }
        result = convert_spell_to_ddb(spell)
        assert result["origin_id"] == 4, "Sight should be origin ID 4"
        assert result["range"] == 0, "Sight range should be 0"


class TestDuration:
    """Test duration mapping"""

    def test_instantaneous(self):
        spell = {
            "name": "Test",
            "level": 0,
            "duration": [{"type": "instant"}]
        }
        result = convert_spell_to_ddb(spell)
        assert result["duration_id"] == 1, "Instantaneous should be ID 1"
        assert result["duration_interval"] == "", "Instantaneous should have empty interval"
        assert result["duration_unit"] == "", "Instantaneous should have empty unit"

    def test_timed_1_round(self):
        spell = {
            "name": "Test",
            "level": 0,
            "duration": [{"type": "timed", "duration": {"type": "rounds", "amount": 1}}]
        }
        result = convert_spell_to_ddb(spell)
        assert result["duration_id"] == 3, "Timed should be ID 3"
        assert result["duration_interval"] == "1", "Should be '1' round"
        assert result["duration_unit"] == "1", "Round should be unit ID '1'"

    def test_concentration_1_minute(self):
        spell = {
            "name": "Test",
            "level": 0,
            "duration": [{"type": "timed", "concentration": True, "duration": {"type": "minute", "amount": 1}}]
        }
        result = convert_spell_to_ddb(spell)
        assert result["duration_id"] == 2, "Concentration should be ID 2"
        assert result["duration_interval"] == "1", "Should be '1' minute"
        assert result["duration_unit"] == "2", "Minute should be unit ID '2'"

    def test_timed_10_minutes(self):
        spell = {
            "name": "Test",
            "level": 0,
            "duration": [{"type": "timed", "duration": {"type": "minutes", "amount": 10}}]
        }
        result = convert_spell_to_ddb(spell)
        assert result["duration_id"] == 3, "Timed should be ID 3"
        assert result["duration_interval"] == "10", "Should be '10' minutes"
        assert result["duration_unit"] == "2", "Minute should be unit ID '2'"

    def test_until_dispelled(self):
        spell = {
            "name": "Test",
            "level": 0,
            "duration": [{"type": "permanent", "ends": ["dispel"]}]
        }
        result = convert_spell_to_ddb(spell)
        assert result["duration_id"] == 5, "Until dispelled should be ID 5"
        assert result["duration_interval"] == "", "Should have empty interval"
        assert result["duration_unit"] == "", "Should have empty unit"


class TestComponents:
    """Test component mapping"""

    def test_verbal_somatic(self):
        spell = {
            "name": "Test",
            "level": 0,
            "components": {"v": True, "s": True}
        }
        result = convert_spell_to_ddb(spell)
        assert result["verbal"] is True
        assert result["somatic"] is True
        assert result["material"] is False

    def test_all_components(self):
        spell = {
            "name": "Test",
            "level": 0,
            "components": {"v": True, "s": True, "m": True}
        }
        result = convert_spell_to_ddb(spell)
        assert result["verbal"] is True
        assert result["somatic"] is True
        assert result["material"] is True

    def test_no_components(self):
        spell = {
            "name": "Test",
            "level": 0,
            "components": {}
        }
        result = convert_spell_to_ddb(spell)
        assert result["verbal"] is False
        assert result["somatic"] is False
        assert result["material"] is False


class TestClasses:
    """Test class ID mapping"""

    def test_sorcerer_wizard(self):
        spell = {
            "name": "Test",
            "level": 0,
            "classes": {
                "fromClassList": [
                    {"name": "Sorceror"},  # Typo version
                    {"name": "Wizard"}
                ]
            }
        }
        result = convert_spell_to_ddb(spell)
        assert 2190884 in result["classes"], "Should include Sorcerer ID 2190884"
        assert 2190886 in result["classes"], "Should include Wizard ID 2190886"

    def test_sorcerer_spelling_variants(self):
        # Test both correct spelling and typo
        spell1 = {
            "name": "Test",
            "level": 0,
            "classes": {"fromClassList": [{"name": "Sorcerer"}]}
        }
        spell2 = {
            "name": "Test",
            "level": 0,
            "classes": {"fromClassList": [{"name": "Sorceror"}]}
        }
        result1 = convert_spell_to_ddb(spell1)
        result2 = convert_spell_to_ddb(spell2)
        assert result1["classes"] == [2190884]
        assert result2["classes"] == [2190884]

    def test_all_base_classes(self):
        expected_ids = {
            "artificer": 2656866,
            "bard": 2190876,
            "cleric": 2190877,
            "druid": 2190878,
            "paladin": 2190881,
            "ranger": 2190882,
            "sorcerer": 2190884,
            "warlock": 2190885,
            "wizard": 2190886
        }
        for class_name, expected_id in expected_ids.items():
            spell = {
                "name": "Test",
                "level": 0,
                "classes": {"fromClassList": [{"name": class_name.capitalize()}]}
            }
            result = convert_spell_to_ddb(spell)
            assert expected_id in result["classes"], f"{class_name} should have ID {expected_id}"


class TestHigherLevelCasting:
    """Test higher level casting"""

    def test_no_higher_level(self):
        spell = {"name": "Test", "level": 0}
        result = convert_spell_to_ddb(spell)
        assert result["can_cast_at_higher_level"] is False
        assert result["higher_level_scale"] == 0

    def test_with_higher_level(self):
        spell = {
            "name": "Test",
            "level": 1,
            "entriesHigherLevel": [{"type": "entries", "name": "At Higher Levels", "entries": ["Test"]}]
        }
        result = convert_spell_to_ddb(spell)
        assert result["can_cast_at_higher_level"] is True
        assert result["higher_level_scale"] == 3


class TestRealSpellCases:
    """Test with actual spell data from spreadsheet"""

    def test_blink_and_you_missed_it(self):
        # Real spell from user's data
        spell = {
            "name": "Blink and You Missed It",
            "level": 0,
            "school": "T",
            "range": {"type": "point", "distance": {"type": "self"}},
            "duration": [{"type": "timed", "duration": {"type": "rounds", "amount": 1}}],
            "components": {"v": True, "s": True},
            "classes": {
                "fromClassList": [
                    {"name": "Sorceror"},
                    {"name": "Wizard"}
                ]
            }
        }
        result = convert_spell_to_ddb(spell)

        # Critical assertions
        assert result["school_id"] == 10, "Transmutation"
        assert result["origin_id"] == 1, "Self"
        assert result["range"] == 0, "Range 0 for self"
        assert result["duration_id"] == 3, "Timed"
        assert result["duration_interval"] == "1"
        assert result["duration_unit"] == "1", "Rounds"
        assert result["classes"] == [2190884, 2190886], "Sorcerer + Wizard"

    def test_cauterize_through_time(self):
        spell = {
            "name": "Cauterize Through Time",
            "level": 0,
            "school": "V",
            "range": {"type": "point", "distance": {"type": "feet", "amount": 30.0}},
            "duration": [{"type": "timed", "duration": {"type": "rounds", "amount": 1}}],
            "classes": {
                "fromClassList": [
                    {"name": "Warlock"},
                    {"name": "Sorceror"}
                ]
            }
        }
        result = convert_spell_to_ddb(spell)

        assert result["school_id"] == 7, "Evocation"
        assert result["origin_id"] == 3, "Ranged"
        assert result["range"] == 30, "30 feet as int"
        assert isinstance(result["range"], int), "Range must be int"
        assert result["classes"] == [2190885, 2190884], "Warlock + Sorcerer"

    def test_cinder_veil(self):
        spell = {
            "name": "Cinder Veil",
            "level": 0,
            "school": "V",
            "range": {"type": "point", "distance": {"type": "feet", "amount": 5.0}},
            "duration": [{"type": "timed", "duration": {"type": "rounds", "amount": 1}}],
            "classes": {
                "fromClassList": [
                    {"name": "Cleric"},
                    {"name": "Sorceror"}
                ]
            }
        }
        result = convert_spell_to_ddb(spell)

        assert result["range"] == 5, "5 feet as int"
        assert isinstance(result["range"], int), "Range must be int"


class TestAdditionalFields:
    """Test extraction of additional fields for update endpoints"""

    def test_aoe_cone(self):
        """Should extract cone AOE with size"""
        spell = {
            "name": "Test",
            "level": 0,
            "range": {"type": "cone", "distance": {"type": "feet", "amount": 15}}
        }
        result = convert_spell_to_ddb(spell)

        assert result["aoe_type"] == "1", "Cone should be AOE type 1"
        assert result["aoe_size"] == "15", "AOE size should be 15"

    def test_aoe_sphere(self):
        """Should extract sphere AOE with size"""
        spell = {
            "name": "Test",
            "level": 0,
            "range": {"type": "sphere", "distance": {"type": "feet", "amount": 20}}
        }
        result = convert_spell_to_ddb(spell)

        assert result["aoe_type"] == "5", "Sphere should be AOE type 5"
        assert result["aoe_size"] == "20", "AOE size should be 20"

    def test_save_type_constitution(self):
        """Should detect Constitution saving throw from description"""
        spell = {
            "name": "Test",
            "level": 0,
            "entries": ["The target must make a Constitution saving throw."]
        }
        result = convert_spell_to_ddb(spell)

        assert result["save_type"] == "3", "Should detect Constitution save"

    def test_save_type_dexterity(self):
        """Should detect Dexterity saving throw from description"""
        spell = {
            "name": "Test",
            "level": 0,
            "entries": ["Each creature must succeed on a Dexterity save."]
        }
        result = convert_spell_to_ddb(spell)

        assert result["save_type"] == "2", "Should detect Dexterity save"

    def test_attack_type_ranged(self):
        """Should detect ranged spell attack from description"""
        spell = {
            "name": "Test",
            "level": 0,
            "entries": ["Make a ranged spell attack against the target."]
        }
        result = convert_spell_to_ddb(spell)

        assert result["attack_type"] == "1", "Should detect ranged spell attack"

    def test_attack_type_melee(self):
        """Should detect melee spell attack from description"""
        spell = {
            "name": "Test",
            "level": 0,
            "entries": ["Make a melee spell attack against the target."]
        }
        result = convert_spell_to_ddb(spell)

        assert result["attack_type"] == "2", "Should detect melee spell attack"

    def test_no_aoe_type(self):
        """Should have empty AOE type for spells without AOE"""
        spell = {
            "name": "Test",
            "level": 0,
            "range": {"type": "point", "distance": {"type": "touch"}}
        }
        result = convert_spell_to_ddb(spell)

        assert result["aoe_type"] == "", "Should have no AOE type"
        assert result["aoe_size"] == "", "Should have no AOE size"

    def test_no_save_or_attack(self):
        """Should have empty save/attack for utility spells"""
        spell = {
            "name": "Test",
            "level": 0,
            "entries": ["You create a minor magical effect."]
        }
        result = convert_spell_to_ddb(spell)

        assert result["save_type"] == "", "Should have no save type"
        assert result["attack_type"] == "", "Should have no attack type"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
