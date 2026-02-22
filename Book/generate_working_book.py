"""
Generate a complete PHB with species, classes (with subclasses), and more.
"""

import sys
sys.path.insert(0, '..')

from Book.book_api import BookAPI
from Book.google_docs_client import GoogleDocsClient
from Book.writers.complete_phb import CompletePHBWriter
from FiveETools.gsheets_client import fantasy_sheets, modern_sheets

# Configuration
DOC_ID = "1_a0yx9UnrsE4oPdkDS1WSkF1nvf-L4PV4bSDKluSI-w"
CREDENTIALS_PATH = "../FiveETools/key.json"

# Choose source: "fantasy" or "modern"
SOURCE = "modern"  # Change to "modern" for Vestigium setting


print("=" * 80)
print("Complete Player's Handbook Generator")
print("=" * 80)
print()
print(f"Source: {SOURCE.upper()}")
print()

# Initialize
print("Initializing clients...")
gdocs = GoogleDocsClient(DOC_ID, CREDENTIALS_PATH)

# Select appropriate sheets client
gsheets = fantasy_sheets if SOURCE == "fantasy" else modern_sheets

book_api = BookAPI(gdocs, gsheets)
print("✓ Clients initialized")
print()

# Generate book
print("Generating complete PHB...")
print("-" * 80)

writer = CompletePHBWriter(book_api, source=SOURCE)

# Special handling for classes with subclasses
if SOURCE == "modern":
    # Override generate_book to handle classes specially
    print("Starting book generation...")

    # Clear existing content
    print("Clearing document...")
    gdocs.clear_document()

    # Generate content
    all_lines = []

    # Cover page
    print("Adding cover page...")
    all_lines.extend(writer.write_cover_page())

    # Table of contents
    print("Adding table of contents...")
    all_lines.extend(writer.write_table_of_contents())

    # Process regular sections
    sections = writer.get_sections()

    for section_name, entity_type, filter_func in sections:
        print(f"Processing section: {section_name}...")

        try:
            entities = book_api.load_entities(entity_type, source=SOURCE)

            if filter_func:
                entities = filter_func(entities)

            formatter = writer.get_formatter(entity_type)
            section_lines = writer.write_section_with_error_handling(
                section_name, entities, formatter
            )
            all_lines.extend(section_lines)

        except Exception as e:
            print(f"  Error processing {section_name}: {e}")
            continue

    # Add classes with subclasses
    print("Processing section: Classes (with subclasses)...")
    classes_lines = writer.write_classes_with_subclasses()
    all_lines.extend(classes_lines)

    # Write all content
    print("Writing content to Google Docs...")
    book_api._write_lines_to_doc(all_lines)

    # Apply two-column layout
    print("Applying PHB-style layout...")
    gdocs.apply_two_column_layout()

    print("Book generation complete!")
else:
    # For fantasy, use standard generation (no classes)
    book_api.generate_book(writer, DOC_ID)

print()
print("=" * 80)
print("✓ Book generation complete!")
print("=" * 80)
print()
print(f"View at: https://docs.google.com/document/d/{DOC_ID}/edit")
print()

if SOURCE == "fantasy":
    print("The book contains:")
    print("  - Species (fantasy races)")
    print("  - Spells (sorted by level)")
    print("  - Languages")
else:
    print("The book contains:")
    print("  - Species")
    print("  - Classes (with subclasses nested under each class)")
    print("  - Backgrounds")
    print("  - Feats")
    print("  - Spells (sorted by level)")
    print("  - Items")
    print("  - Languages")
