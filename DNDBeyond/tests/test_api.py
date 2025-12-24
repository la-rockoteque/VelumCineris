"""Unit tests for D&D Beyond API"""
import pytest
from unittest.mock import Mock, MagicMock, patch
import sys
sys.path.insert(0, '/Users/rocko/dev/Perso/VestigiumFoundrySpells')

from DNDBeyond.helpers.DnDBeyondAPI import DnDBeyondAPI


class TestAPIFormData:
    """Test that API sends correct form data"""

    def setup_method(self):
        self.session = Mock()
        self.api = DnDBeyondAPI(self.session, "test_security", "test_auth")

    def test_spell_range_empty_for_zero(self):
        """spell-range should be empty string when range is 0"""
        data = {
            "name": "Test",
            "level": 0,
            "school_id": 7,
            "origin_id": 1,
            "range": 0,  # Self range
            "classes": []
        }

        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 303
        mock_response.headers = {"location": "/homebrew/creations/spells/12345-test/edit"}
        self.session.post = Mock(return_value=mock_response)

        self.api.create_spell(data)

        # Get the form_data that was sent
        call_args = self.session.post.call_args
        form_data = call_args[1]['data']

        assert form_data["spell-range"] == "", "spell-range must be empty string for range=0"

    def test_spell_range_value_for_nonzero(self):
        """spell-range should be string of number when range > 0"""
        data = {
            "name": "Test",
            "level": 0,
            "school_id": 7,
            "origin_id": 3,
            "range": 30,  # 30 feet
            "classes": []
        }

        mock_response = Mock()
        mock_response.status_code = 303
        mock_response.headers = {"location": "/homebrew/creations/spells/12345-test/edit"}
        self.session.post = Mock(return_value=mock_response)

        self.api.create_spell(data)

        call_args = self.session.post.call_args
        form_data = call_args[1]['data']

        assert form_data["spell-range"] == "30", "spell-range should be '30'"

    def test_higher_level_scale_always_sent(self):
        """higher-level-scale should always be sent, even if empty"""
        data = {
            "name": "Test",
            "level": 0,
            "school_id": 7,
            "can_cast_at_higher_level": False,
            "higher_level_scale": 0,
            "classes": []
        }

        mock_response = Mock()
        mock_response.status_code = 303
        mock_response.headers = {"location": "/homebrew/creations/spells/12345-test/edit"}
        self.session.post = Mock(return_value=mock_response)

        self.api.create_spell(data)

        call_args = self.session.post.call_args
        form_data = call_args[1]['data']

        assert "higher-level-scale" in form_data, "higher-level-scale must always be present"
        assert form_data["higher-level-scale"] == "", "should be empty when not casting at higher level"

    def test_higher_level_scale_with_value(self):
        """higher-level-scale should have value when can_cast is true"""
        data = {
            "name": "Test",
            "level": 1,
            "school_id": 7,
            "can_cast_at_higher_level": True,
            "higher_level_scale": 3,
            "classes": []
        }

        mock_response = Mock()
        mock_response.status_code = 303
        mock_response.headers = {"location": "/homebrew/creations/spells/12345-test/edit"}
        self.session.post = Mock(return_value=mock_response)

        self.api.create_spell(data)

        call_args = self.session.post.call_args
        form_data = call_args[1]['data']

        assert form_data["higher-level-scale"] == "3"

    def test_class_mapping_multipart(self):
        """class-mapping should be sent as multipart files"""
        data = {
            "name": "Test",
            "level": 0,
            "school_id": 7,
            "classes": [2190884, 2190886]  # Sorcerer, Wizard
        }

        mock_response = Mock()
        mock_response.status_code = 303
        mock_response.headers = {"location": "/homebrew/creations/spells/12345-test/edit"}
        self.session.post = Mock(return_value=mock_response)

        self.api.create_spell(data)

        call_args = self.session.post.call_args
        files = call_args[1]['files']

        assert len(files) == 2, "Should have 2 class mappings"
        assert files[0] == ("class-mapping", (None, "2190884"))
        assert files[1] == ("class-mapping", (None, "2190886"))

    def test_duration_fields(self):
        """Duration interval and unit should be strings"""
        data = {
            "name": "Test",
            "level": 0,
            "school_id": 7,
            "duration_id": 3,
            "duration_interval": "1",  # String
            "duration_unit": "1",      # String
            "classes": []
        }

        mock_response = Mock()
        mock_response.status_code = 303
        mock_response.headers = {"location": "/homebrew/creations/spells/12345-test/edit"}
        self.session.post = Mock(return_value=mock_response)

        self.api.create_spell(data)

        call_args = self.session.post.call_args
        form_data = call_args[1]['data']

        assert form_data["spell-duration-interval"] == "1"
        assert form_data["spell-duration-unit"] == "1"


class TestAPIResponseHandling:
    """Test API response handling"""

    def setup_method(self):
        self.session = Mock()
        self.api = DnDBeyondAPI(self.session, "test_security", "test_auth")

    def test_success_303_redirect(self):
        """Should extract spell ID from 303 redirect location header"""
        data = {"name": "Test", "level": 0, "school_id": 7, "classes": []}

        mock_response = Mock()
        mock_response.status_code = 303
        mock_response.headers = {"location": "/homebrew/creations/spells/12345-test-spell/edit"}
        self.session.post = Mock(return_value=mock_response)

        spell_id = self.api.create_spell(data)

        assert spell_id == "12345"

    def test_failure_200_silent(self):
        """Should return None on 200 (form validation failure)"""
        data = {"name": "Test", "level": 0, "school_id": 7, "classes": []}

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.reason = "OK"
        mock_response.text = "<html>...</html>"
        mock_response.headers = {"content-type": "text/html"}
        self.session.post = Mock(return_value=mock_response)

        spell_id = self.api.create_spell(data)

        assert spell_id is None
        assert self.api.last_error is not None

    def test_failure_400_error(self):
        """Should handle 400 errors"""
        data = {"name": "Test", "level": 0, "school_id": 7, "classes": []}

        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.reason = "Bad Request"
        mock_response.text = "Invalid data"
        mock_response.headers = {"content-type": "text/plain"}
        self.session.post = Mock(return_value=mock_response)

        spell_id = self.api.create_spell(data)

        assert spell_id is None
        assert self.api.last_error["status_code"] == 400


class TestFindSpellByName:
    """Test spell lookup by name"""

    def setup_method(self):
        self.session = Mock()
        self.api = DnDBeyondAPI(self.session, "test_security", "test_auth")

    def test_find_exact_match(self):
        """Should find spell with exact name match"""
        user_spells = [
            {"id": "12345", "name": "Fireball"},
            {"id": "67890", "name": "Magic Missile"}
        ]

        spell_id = self.api.find_spell_by_name("Fireball", user_spells)
        assert spell_id == "12345"

    def test_find_case_insensitive(self):
        """Should find spell with case-insensitive match"""
        user_spells = [
            {"id": "12345", "name": "Fireball"}
        ]

        spell_id = self.api.find_spell_by_name("fireball", user_spells)
        assert spell_id == "12345"

        spell_id = self.api.find_spell_by_name("FIREBALL", user_spells)
        assert spell_id == "12345"

    def test_find_with_whitespace(self):
        """Should handle whitespace in names"""
        user_spells = [
            {"id": "12345", "name": "Magic Missile"}
        ]

        spell_id = self.api.find_spell_by_name("  Magic Missile  ", user_spells)
        assert spell_id == "12345"

    def test_not_found(self):
        """Should return None when spell not found"""
        user_spells = [
            {"id": "12345", "name": "Fireball"}
        ]

        spell_id = self.api.find_spell_by_name("Lightning Bolt", user_spells)
        assert spell_id is None


class TestSpellUpdateEndpoints:
    """Test spell update endpoints (basic_information, higher_level, modifier, condition)"""

    def setup_method(self):
        self.session = Mock()
        self.api = DnDBeyondAPI(self.session, "test_security", "test_auth")

    def test_update_basic_information_success(self):
        """Should successfully update basic information"""
        spell_id = "3135829"
        slug = "ashen-breath"
        data = {
            "name": "Ashen Breath",
            "level": 0,
            "school_id": 7,
            "aoe_type": "1",  # Cone
            "aoe_size": "15",
            "save_type": "3",  # Constitution
            "classes": [2190884]
        }

        mock_response = Mock()
        mock_response.status_code = 303
        self.session.post = Mock(return_value=mock_response)

        result = self.api.update_basic_information(spell_id, slug, data)

        assert result is True
        call_args = self.session.post.call_args
        form_data = call_args[1]['data']

        assert form_data["spell-aoe"] == "1"
        assert form_data["spell-aoe-size"] == "15"
        assert form_data["spell-save-type"] == "3"

    def test_create_higher_level_success(self):
        """Should successfully create higher level scaling"""
        spell_id = "3135829"
        level_data = {
            "level": "",  # Scales per slot level
            "modifier": "",
            "effect_type": "16",  # Damage
            "dice_count": "1",
            "dice_value": "8",
            "dice_fixed": "",
            "dice_details": "fire"
        }

        mock_response = Mock()
        mock_response.status_code = 303
        self.session.post = Mock(return_value=mock_response)

        result = self.api.create_higher_level(spell_id, level_data)

        assert result is True
        call_args = self.session.post.call_args
        form_data = call_args[1]['data']

        assert form_data["effect-type"] == "16"
        assert form_data["dice-count"] == "1"
        assert form_data["dice-value"] == "8"
        assert form_data["dice-details"] == "fire"

    def test_create_modifier_success(self):
        """Should successfully create a spell modifier"""
        spell_id = "3135829"
        modifier_data = {
            "modifier_type": "3",  # Bonus
            "modifier_sub_type": "68",  # AC
            "fixed_value": "2",
            "duration": "1",
            "duration_unit": "3",  # Hours
        }

        mock_response = Mock()
        mock_response.status_code = 303
        self.session.post = Mock(return_value=mock_response)

        result = self.api.create_modifier(spell_id, modifier_data)

        assert result is True
        call_args = self.session.post.call_args
        form_data = call_args[1]['data']

        assert form_data["spell-modifier-type"] == "3"
        assert form_data["spell-modifier-sub-type"] == "68"
        assert form_data["fixed-value"] == "2"

    def test_create_condition_success(self):
        """Should successfully create a spell condition"""
        spell_id = "3135829"
        condition_data = {
            "condition_effect": "1",  # Grants condition
            "condition": "1",  # Blinded
            "condition_duration": "1",
            "duration_unit": "1",  # Rounds
        }

        mock_response = Mock()
        mock_response.status_code = 303
        self.session.post = Mock(return_value=mock_response)

        result = self.api.create_condition(spell_id, condition_data)

        assert result is True
        call_args = self.session.post.call_args
        form_data = call_args[1]['data']

        assert form_data["condition-effect"] == "1"
        assert form_data["condition"] == "1"
        assert form_data["condition-duration"] == "1"

    def test_create_slug(self):
        """Should create proper URL slugs from spell names"""
        assert DnDBeyondAPI.create_slug("Fireball") == "fireball"
        assert DnDBeyondAPI.create_slug("Ashen Breath") == "ashen-breath"
        assert DnDBeyondAPI.create_slug("Blink and You Missed It") == "blink-and-you-missed-it"
        assert DnDBeyondAPI.create_slug("  Magic   Missile  ") == "magic-missile"
        assert DnDBeyondAPI.create_slug("Tasha's Hideous Laughter") == "tasha-s-hideous-laughter"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
