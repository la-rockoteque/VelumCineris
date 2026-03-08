#!/usr/bin/env python3
"""Quick test to verify API paths and show what's being sent."""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parents[1]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

print("=" * 80)
print("API PATHS TEST")
print("=" * 80)
print()

# Test data
test_spell_id = "3135829"
test_modifier_data = {
    "type": "3",  # Damage modifier
    "subtype": "68",
    "dice_count": "2",
    "dice_type": "8",
    "fixed_value": "12",
    "duration": "12",
    "duration_unit": "2",
    "restriction": "Test restriction"
}

test_condition_data = {
    "condition_effect": "1",
    "condition": "1",
    "condition_duration": "",
    "duration_unit": "",
    "condition_exception": ""
}

test_higher_level_data = {
    "level": "3",
    "modifier": "",
    "effect_type": "16",
    "dice_count": "1",
    "dice_value": "6",
    "dice_fixed": "",
    "dice_details": "Extra 1d6 damage"
}

print("TEST PATHS:")
print("-" * 80)
print(f"Modifier CREATE:  POST /spells/modifier/create/{test_spell_id}")
print(f"Modifier DELETE:  POST /spells/modifier/{{modifier_id}}/delete")
print()
print(f"Condition CREATE: POST /spells/condition/create/{test_spell_id}")
print(f"Condition DELETE: POST /spells/condition/{{condition_id}}/delete")
print()
print(f"Higher Level CREATE: POST /spells/additional/create/{test_spell_id}")
print(f"Higher Level DELETE: POST /spells/additional/{{level_id}}/delete")
print()

print("TEST FORM DATA:")
print("-" * 80)
print("\nModifier:")
for key, val in test_modifier_data.items():
    print(f"  {key}: {val}")

print("\nCondition:")
for key, val in test_condition_data.items():
    print(f"  {key}: {val}")

print("\nHigher Level:")
for key, val in test_higher_level_data.items():
    print(f"  {key}: {val}")

print()
print("=" * 80)
print("Now run Cell 14 and check the DEBUG output to see actual requests")
print("=" * 80)
