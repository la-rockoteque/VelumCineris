# Spell Publishing & Version Tracking Guide

## Overview

The sync notebook now supports tracking and managing **publish status** and **version numbers** for D&D Beyond spells.

## Spreadsheet Columns

Three new columns are automatically tracked:

### 1. Version Tracking
- **Column**: `DDB Version`
- **Description**: Version number for homebrew tracking
- **Format**: Any string (e.g., "1.0", "1.2", "A", "B", etc.)
- **Usage**: Synced to D&D Beyond during spell creation/update

### 2. Publish Status Tracking
- **Column**: `DDB Publish Status`
- **Values**:
  - `Published` (1) - Visible to public
  - `Draft` (2) - Private, only visible to you
- **Usage**: Updated when fetching spell details or publishing

### 3. Sync Status (Already Implemented)
- **Column**: `DDB Sync Status`
- **Values**: ✅ (success), ❌ (failure)

## Publish States

D&D Beyond homebrew spells have two states:

### Draft (Private)
- Status code: `2`
- Only visible to you
- Can be edited freely
- Default state for newly created spells

### Published (Public)
- Status code: `1`
- Visible in public homebrew listings
- Can be added to other users' collections
- Subject to D&D Beyond moderation

## Using Version Numbers

Add a "DDB Version" column to your Google Sheets with version strings:

```
Spell Name              | DDB Version
------------------------|-------------
Fireball                | 1.0
Magic Missile           | 2.1
Custom Spell            | A
```

Versions will be automatically synced when creating or updating spells.

## Publishing Spells

### Method 1: Batch Publish (Recommended)

Use the new publishing cell in the notebook:

```python
# Configure which spells to publish
PUBLISH_FILTER = lambda spell: spell["name"] in ["Fireball", "Magic Missile"]

# Or publish all synced spells
PUBLISH_FILTER = lambda spell: True

# Run the publish cell
```

### Method 2: Manual via API

```python
from DNDBeyond.helpers import DnDBeyondAPI, normalize_ddb_id

# Publish a spell
spell_id = "3137383"
success = ddb_api.publish_spell(spell_id)

# Unpublish a spell (make it draft again)
success = ddb_api.unpublish_spell(spell_id)
```

### Method 3: Check Status

```python
# Get spell details including publish status and version
slug = DnDBeyondAPI.create_slug("Fireball")
details = ddb_api.get_spell_details("3137383", slug)

print(f"Version: {details.get('version', 'N/A')}")
print(f"Status: {details.get('status')} (1=Published, 2=Draft)")
```

## Workflow Examples

### Example 1: Initial Creation (Draft)
1. Create spells via sync notebook (cell-13)
2. Spells are created as **Draft** (private)
3. Test in Character Builder
4. When ready, publish via publishing cell

### Example 2: Update with Version Bump
1. Update "DDB Version" column in spreadsheet (e.g., "1.0" → "1.1")
2. Run sync with `UPDATE_EXISTING=True`
3. Version number is updated on D&D Beyond
4. Publish status remains unchanged

### Example 3: Bulk Publish
1. Sync all spells to D&D Beyond (creates as drafts)
2. Review spells on D&D Beyond
3. Use publishing cell to publish all or selected spells
4. Spreadsheet is updated with publish status

### Example 4: Unpublish for Major Changes
1. Use unpublish to make a published spell private
2. Make major edits
3. Test changes
4. Re-publish when ready

## API Methods

### New Methods in `DnDBeyondAPI`

```python
# Get spell details (version and publish status)
get_spell_details(spell_id: str, slug: str) -> dict

# Publish a spell (make public)
publish_spell(spell_id: str) -> bool

# Unpublish a spell (make private)
unpublish_spell(spell_id: str) -> bool
```

### Returns

**get_spell_details()** returns:
```python
{
    'version': '1.0',
    'status': 1  # 1=Published, 2=Draft
}
```

**publish_spell() / unpublish_spell()** return:
- `True` if successful
- `False` if failed

## Filtering Spells by Status

When fetching existing spells, you can filter by status:

```python
# Get only published spells
published_spells = ddb_api.spells.list(status="1")

# Get only draft spells
draft_spells = ddb_api.spells.list(status="2")

# Get all spells (default)
all_spells = ddb_api.spells.list(status=None)
```

## Troubleshooting

### Version Not Syncing
- Ensure "DDB Version" column exists in spreadsheet
- Check that version field is populated
- Verify converter includes version in conversion

### Publish Status Not Updating
- Check D&D Beyond session cookies are valid
- Ensure security tokens are current
- Verify spell ID exists and is correct

### Can't Publish Spell
- Spell must be created first (have DDB ID)
- Security tokens must be valid
- Check D&D Beyond homebrew guidelines

## Important Notes

⚠️ **Publishing Visibility**:
- Published spells are publicly visible
- Cannot be unpublished if already approved by moderators
- May be subject to content review

⚠️ **Version Changes**:
- Version is a free-form text field
- No validation is performed
- Use consistent format for tracking

⚠️ **Status Tracking**:
- Publish status is fetched from D&D Beyond edit page
- May require additional API call
- Cached in spreadsheet for performance

## Best Practices

1. **Use semantic versioning**: "1.0", "1.1", "2.0"
2. **Test as drafts first**: Always test spells before publishing
3. **Version on updates**: Bump version when making changes
4. **Document changes**: Use version to track major revisions
5. **Batch operations**: Publish multiple spells at once for efficiency
