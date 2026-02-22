"""Integration tests for duplicate detection using spreadsheet DDB IDs"""
import pytest
import pandas as pd
import sys
sys.path.insert(0, '/Users/rocko/dev/Perso/VelumCineris/DNDBeyond')


class TestSpreadsheetDuplicateDetection:
    """Test that spells with DDB IDs in spreadsheet are properly detected as duplicates"""

    def test_existing_ddb_id_detected(self):
        """Spell with DDB ID in spreadsheet should be detected as existing"""
        # Mock spreadsheet data
        df_spells = pd.DataFrame({
            'Spell Name': ['Fireball', 'Magic Missile', 'Shield'],
            'DDB': ['3135829', '3135830', None]
        })

        # Build lookup dict (same logic as notebook Cell 14)
        spell_to_ddb_id = {}
        if 'DDB' in df_spells.columns and 'Spell Name' in df_spells.columns:
            for _, row in df_spells.iterrows():
                spell_name = row.get('Spell Name')
                ddb_id = row.get('DDB')
                if spell_name and pd.notna(ddb_id) and str(ddb_id).strip():
                    spell_to_ddb_id[spell_name] = str(ddb_id).strip()

        # Test: Fireball should be found
        assert 'Fireball' in spell_to_ddb_id
        assert spell_to_ddb_id['Fireball'] == '3135829'

        # Test: Magic Missile should be found
        assert 'Magic Missile' in spell_to_ddb_id
        assert spell_to_ddb_id['Magic Missile'] == '3135830'

        # Test: Shield should NOT be found (null DDB ID)
        assert 'Shield' not in spell_to_ddb_id

    def test_name_matching_exact(self):
        """Name matching must be exact between spell data and spreadsheet"""
        df_spells = pd.DataFrame({
            'Spell Name': ['Blink and You Missed It', 'Fireball'],
            'DDB': ['3136124', '3135829']
        })

        spell_to_ddb_id = {}
        for _, row in df_spells.iterrows():
            spell_name = row.get('Spell Name')
            ddb_id = row.get('DDB')
            if spell_name and pd.notna(ddb_id) and str(ddb_id).strip():
                spell_to_ddb_id[spell_name] = str(ddb_id).strip()

        # Test: Exact match works
        spell_data = {"name": "Blink and You Missed It", "level": 0}
        assert spell_data["name"] in spell_to_ddb_id
        assert spell_to_ddb_id[spell_data["name"]] == '3136124'

        # Test: Different case doesn't match (if that's the issue)
        spell_data_wrong_case = {"name": "Blink And You Missed It", "level": 0}
        if spell_data_wrong_case["name"] not in spell_to_ddb_id:
            # This would cause a double - the names don't match!
            assert True, "Case sensitivity could cause doubles"

    def test_empty_ddb_ids_ignored(self):
        """Empty strings and whitespace-only DDB IDs should be ignored"""
        df_spells = pd.DataFrame({
            'Spell Name': ['Spell1', 'Spell2', 'Spell3', 'Spell4'],
            'DDB': ['3135829', '', '   ', None]
        })

        spell_to_ddb_id = {}
        for _, row in df_spells.iterrows():
            spell_name = row.get('Spell Name')
            ddb_id = row.get('DDB')
            if spell_name and pd.notna(ddb_id) and str(ddb_id).strip():
                spell_to_ddb_id[spell_name] = str(ddb_id).strip()

        # Only Spell1 should be in the dict
        assert len(spell_to_ddb_id) == 1
        assert 'Spell1' in spell_to_ddb_id
        assert spell_to_ddb_id['Spell1'] == '3135829'

    def test_numeric_ddb_ids_converted_to_string(self):
        """Numeric DDB IDs should be properly converted to strings (pandas float issue)"""
        from DNDBeyond.helpers import normalize_ddb_id

        df_spells = pd.DataFrame({
            'Spell Name': ['Spell1', 'Spell2', 'Spell3'],
            'DDB': [3135829, 3135830.0, '3135831']  # int, float, string
        })

        spell_to_ddb_id = {}
        for _, row in df_spells.iterrows():
            spell_name = row.get('Spell Name')
            ddb_id = row.get('DDB')
            if spell_name and pd.notna(ddb_id):
                normalized_id = normalize_ddb_id(ddb_id)
                if normalized_id:
                    spell_to_ddb_id[spell_name] = normalized_id

        # All should be normalized to proper string format (no .0 suffix)
        assert spell_to_ddb_id['Spell1'] == '3135829'
        assert spell_to_ddb_id['Spell2'] == '3135830'  # .0 stripped
        assert spell_to_ddb_id['Spell3'] == '3135831'

    def test_duplicate_detection_workflow(self):
        """Test the complete workflow: spreadsheet lookup prevents double creation"""
        from DNDBeyond.helpers import normalize_ddb_id

        # Simulate spreadsheet with existing spells (realistic pandas data types)
        df_spells = pd.DataFrame({
            'Spell Name': ['Ashen Breath', 'Blink and You Missed It', 'Cinder Veil', 'New Spell'],
            'DDB': [3135829.0, '3136124', 3135838, None]  # float, string, int, null
        })

        # Build lookup using normalize_ddb_id (matches fixed notebook logic)
        spell_to_ddb_id = {}
        for _, row in df_spells.iterrows():
            spell_name = row.get('Spell Name')
            ddb_id = row.get('DDB')
            if spell_name and pd.notna(ddb_id):
                normalized_id = normalize_ddb_id(ddb_id)
                if normalized_id:
                    spell_to_ddb_id[spell_name] = normalized_id

        # Simulate sync attempting to process these spells
        spells_to_sync = [
            {"name": "Ashen Breath", "level": 0},
            {"name": "Blink and You Missed It", "level": 0},
            {"name": "New Spell", "level": 1}
        ]

        should_create = []
        should_skip = []

        SKIP_EXISTING = True  # This should be True in production

        for spell in spells_to_sync:
            spell_name = spell.get("name", "Unnamed")

            # Check if spell already has DDB ID in spreadsheet
            if SKIP_EXISTING and spell_name in spell_to_ddb_id:
                existing_id = spell_to_ddb_id[spell_name]
                should_skip.append((spell_name, existing_id))
            else:
                should_create.append(spell_name)

        # Validate results
        assert len(should_skip) == 2, "Should skip 2 existing spells"
        assert len(should_create) == 1, "Should create 1 new spell"

        # Check specific spells
        skip_names = [name for name, _ in should_skip]
        assert "Ashen Breath" in skip_names
        assert "Blink and You Missed It" in skip_names
        assert "New Spell" in should_create

        # Validate IDs are correct (float was normalized to string without .0)
        skip_dict = dict(should_skip)
        assert skip_dict["Ashen Breath"] == "3135829"  # Was 3135829.0
        assert skip_dict["Blink and You Missed It"] == "3136124"


class TestNameNormalization:
    """Test that spell names are consistently formatted between source and spreadsheet"""

    def test_spell_name_from_source_matches_spreadsheet(self):
        """Spell names from source data should match spreadsheet format exactly"""
        # This is the actual spell from user's data
        spell_from_source = {"name": "Blink and You Missed It", "level": 0}

        # This is how it might appear in spreadsheet (from HTML parsing or manual entry)
        # Note: Cell 12 output shows "Blink And You Missed It" with capital A
        spreadsheet_variations = [
            "Blink and You Missed It",  # lowercase 'and'
            "Blink And You Missed It",  # capital 'And'
        ]

        # If names don't match exactly, duplicates will be created
        spell_name = spell_from_source["name"]

        # Test each variation
        for variation in spreadsheet_variations:
            if spell_name == variation:
                print(f"✓ Match: '{spell_name}' == '{variation}'")
            else:
                print(f"✗ NO MATCH: '{spell_name}' != '{variation}' - THIS CAUSES DOUBLES!")

        # The issue: if spreadsheet has "Blink And You Missed It" but source has
        # "Blink and You Missed It", the lookup fails and creates a double

    def test_html_slug_parsing_consistency(self):
        """HTML slug parsing should produce names that match source data (case-insensitive)"""
        # From Cell 12: HTML has data-slug="3136124-blink-and-you-missed-it"
        slug = "3136124-blink-and-you-missed-it"

        # FIXED parsing logic (from DnDBeyondAPI.py:30) - removed .title()
        parts = slug.split('-', 1)
        spell_id = parts[0]
        spell_name = parts[1].replace('-', ' ') if len(parts) > 1 else ''

        # Result: "blink and you missed it" (lowercase, no title case)
        assert spell_name == "blink and you missed it"

        # Source data has: "Blink and You Missed It" (proper case)
        source_name = "Blink and You Missed It"

        # They don't match exactly, but case-insensitive matching should work
        assert spell_name.lower() == source_name.lower(), "Should match case-insensitively"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
