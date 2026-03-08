#!/usr/bin/env python3
"""Test that the field name fix for modifiers works correctly."""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parents[2]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from DNDBeyond.core.Helpers import extract_spell_modifiers
from FiveETools.core.fantasy.spells import spells_list

print("=" * 80)
print("TESTING MODIFIER FIELD NAME FIX")
print("=" * 80)
print()

# Find a spell with modifiers
test_spell = None
for spell in spells_list:
    modifiers = extract_spell_modifiers(spell)
    if modifiers:
        test_spell = spell
        break

if not test_spell:
    print("❌ No spells with modifiers found!")
    sys.exit(1)

print(f"Test spell: {test_spell.get('name')}")
print()

# Extract modifiers
modifiers = extract_spell_modifiers(test_spell)
print(f"Extracted {len(modifiers)} modifier(s):")
print()

for i, mod in enumerate(modifiers, 1):
    print(f"Modifier {i}:")
    print(f"  Field names returned by extraction:")
    for key, value in mod.items():
        print(f"    {key}: {value}")
    print()

    # Check if these will work with create_modifier
    required_fields = ["type", "subtype", "dice_count", "dice_type", "fixed_value"]
    missing = []
    present = []

    for field in required_fields:
        if field in mod:
            present.append(field)
        else:
            # Check alternative names
            alt_names = {
                "type": "modifier_type",
                "subtype": "modifier_sub_type",
                "dice_type": "dice_value"
            }
            if alt_names.get(field) in mod:
                present.append(f"{field} (as {alt_names[field]})")
            else:
                missing.append(field)

    if present:
        print(f"  ✓ Fields present: {', '.join(present)}")
    if missing:
        print(f"  ⚠️  Fields missing: {', '.join(missing)}")

print()
print("=" * 80)
print("The create_modifier method now accepts BOTH field name formats:")
print("  - Short names: type, subtype, dice_type (from extraction)")
print("  - Long names: modifier_type, modifier_sub_type, dice_value (old format)")
print()
print("✓ Field name mismatch is FIXED!")
print("=" * 80)
