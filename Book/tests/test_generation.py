"""
Quick test script for book generation with a small dataset.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = PROJECT_ROOT.parent

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from Book.book_api import BookAPI
from Book.google_docs_client import GoogleDocsClient
from Book.core.writers import OmnibookWriter
from Spreadsheet.sheets import fantasy_sheets

# Configuration
DOC_ID = "1_a0yx9UnrsE4oPdkDS1WSkF1nvf-L4PV4bSDKluSI-w"
CREDENTIALS_PATH = str(REPO_ROOT / "FiveETools" / "key.json")
SOURCE = "fantasy"

print("=" * 80)
print("Book Generator - Quick Test")
print("=" * 80)
print()

# Initialize
print("Initializing clients...")
gdocs = GoogleDocsClient(DOC_ID, CREDENTIALS_PATH)
book_api = BookAPI(gdocs, fantasy_sheets)
print("✓ Clients initialized")
print()

# Test 1: Preview spells
print("Test 1: Preview 3 spells")
print("-" * 80)
try:
    book_api.preview_section("spell", source=SOURCE, limit=3)
    print("✓ Spell preview successful")
except Exception as e:
    print(f"✗ Spell preview failed: {e}")
print()

# Test 2: Preview species
print("Test 2: Preview 3 species")
print("-" * 80)
try:
    book_api.preview_section("species", source=SOURCE, limit=3)
    print("✓ Species preview successful")
except Exception as e:
    print(f"✗ Species preview failed: {e}")
print()

# Test 3: Preview monsters
print("Test 3: Preview 3 monsters")
print("-" * 80)
try:
    book_api.preview_section("monster", source=SOURCE, limit=3)
    print("✓ Monster preview successful")
except Exception as e:
    print(f"✗ Monster preview failed: {e}")
print()

# Test 4: Generate small book (first 10 entities per section)
print("Test 4: Generate small test book (10 entities per section)")
print("-" * 80)
try:
    # Create a custom writer with limited entities
    class TestWriter(OmnibookWriter):
        def get_sections(self):
            sections = super().get_sections()
            # Add filter to limit to 10 entities per section
            limited_sections = []
            for name, entity_type, filter_func in sections:
                def limit_filter(entities, func=filter_func):
                    if func:
                        entities = func(entities)
                    return entities[:10]  # Limit to 10
                limited_sections.append((name, entity_type, limit_filter))
            return limited_sections

    writer = TestWriter(book_api, source=SOURCE)
    book_api.generate_book(writer, DOC_ID)
    print("✓ Test book generation successful")
    print(f"\nView at: https://docs.google.com/document/d/{DOC_ID}/edit")
except Exception as e:
    print(f"✗ Test book generation failed: {e}")
    import traceback
    traceback.print_exc()

print()
print("=" * 80)
print("Tests complete!")
print("=" * 80)
