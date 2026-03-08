"""
Quick test to verify species converter works after fixes.
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

print("Testing species converter fixes...")
print("=" * 80)

try:
    from FiveETools.core.fantasy.species import races_list
    print(f"✓ Fantasy species loaded: {len(races_list)} species")

    # Show first species
    if races_list:
        first = races_list[0]
        print(f"\nFirst species: {first.get('name')}")
        print(f"  Size: {first.get('size')}")
        print(f"  Speed: {first.get('speed')}")
        print(f"  Abilities: {first.get('ability')}")
except Exception as e:
    print(f"✗ Fantasy species failed: {e}")
    import traceback
    traceback.print_exc()

print()

try:
    from FiveETools.core.modern.species import races_list as modern_races
    print(f"✓ Modern species loaded: {len(modern_races)} species")

    # Show first species
    if modern_races:
        first = modern_races[0]
        print(f"\nFirst species: {first.get('name')}")
        print(f"  Size: {first.get('size')}")
        print(f"  Speed: {first.get('speed')}")
except Exception as e:
    print(f"✗ Modern species failed: {e}")
    import traceback
    traceback.print_exc()

print()
print("=" * 80)
