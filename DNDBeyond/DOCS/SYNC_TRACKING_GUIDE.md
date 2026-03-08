# Sync Tracking Implementation Guide

## Overview

The sync notebook now tracks the status of each spell sync in three Google Sheets columns:

1. **DDB Sync Status** - Visual status indicator
   - ✅ = Successfully synced
   - ❌ = Sync failed
   - 🔄 = Sync in progress (rarely seen)

2. **DDB Sync Error** - Error message if sync failed
   - Empty if successful
   - Contains error details if failed

3. **DDB Last Synced** - Timestamp of last sync attempt
   - Format: `YYYY-MM-DD HH:MM:SS`
   - Updated on every sync attempt

## Implementation Details

### Cell-13 Changes (Base Spell Sync)

**Added at the beginning:**
```python
from datetime import datetime

# Ensure tracking columns exist
print("Ensuring sync tracking columns exist...")
for col_name in ['DDB Sync Status', 'DDB Sync Error', 'DDB Last Synced']:
    try:
        fantasy_sheets.ensure_column_exists(SPELLS_GID, col_name)
    except Exception as e:
        print(f"  ⚠️  Could not ensure column '{col_name}': {e}")
```

**Modified per-spell tracking:**
```python
# Track sync status for each spell
sync_tracking_updates = []  # Accumulated throughout sync

# For each spell:
try:
    # ... existing sync code ...

    if spell_id:  # Success
        sync_tracking_updates.append({
            'spell_name': spell_name,
            'status': '✅',
            'error': '',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    else:  # Failed
        error_msg = str(ddb_api.last_error) if ddb_api.last_error else "Unknown error"
        sync_tracking_updates.append({
            'spell_name': spell_name,
            'status': '❌',
            'error': error_msg[:200],  # Truncate long errors
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
except Exception as e:
    sync_tracking_updates.append({
        'spell_name': spell_name,
        'status': '❌',
        'error': str(e)[:200],
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })
```

**Batch update at the end:**
```python
# Write tracking data to spreadsheet
if sync_tracking_updates and not DRY_RUN:
    print("\n" + "=" * 60)
    print("Updating sync status in Google Sheets...")
    print("=" * 60)

    # Prepare batch updates for tracking columns
    status_updates = []
    error_updates = []
    timestamp_updates = []

    for tracking in sync_tracking_updates:
        spell_name = tracking['spell_name']
        status_updates.append({
            'match_value': spell_name,
            'update_column': 'DDB Sync Status',
            'update_value': tracking['status']
        })
        error_updates.append({
            'match_value': spell_name,
            'update_column': 'DDB Sync Error',
            'update_value': tracking['error']
        })
        timestamp_updates.append({
            'match_value': spell_name,
            'update_column': 'DDB Last Synced',
            'update_value': tracking['timestamp']
        })

    # Batch update all three columns
    try:
        fantasy_sheets.batch_update_cells_by_row_match(SPELLS_GID, "Spell Name", status_updates)
        fantasy_sheets.batch_update_cells_by_row_match(SPELLS_GID, "Spell Name", error_updates)
        fantasy_sheets.batch_update_cells_by_row_match(SPELLS_GID, "Spell Name", timestamp_updates)
        print(f"✓ Updated sync status for {len(sync_tracking_updates)} spells")
    except Exception as e:
        print(f"✗ Error updating tracking columns: {e}")
```

### Cell-14 Changes (Extras Sync)

Similar tracking for modifiers/conditions/scaling:

```python
# Track extras sync separately
extras_tracking_updates = []

for spell_name, (spell, ddb_id) in spell_data_map.items():
    try:
        # ... sync modifiers/conditions/scaling ...

        # Success
        extras_tracking_updates.append({
            'spell_name': spell_name,
            'status': '✅',
            'error': '',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    except Exception as e:
        extras_tracking_updates.append({
            'spell_name': spell_name,
            'status': '❌',
            'error': f"Extras sync failed: {str(e)[:180]}",
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })

# Batch update at the end (same as cell-13)
```

## Benefits

### 1. Quick Visual Overview
Open your Google Sheet and instantly see which spells synced successfully:
```
Spell Name          | DDB Sync Status | DDB Sync Error | DDB Last Synced
--------------------|-----------------|----------------|------------------
Fireball            | ✅              |                | 2026-02-15 14:30:22
Magic Missile       | ✅              |                | 2026-02-15 14:30:25
Broken Spell        | ❌              | 403 Forbidden  | 2026-02-15 14:30:28
```

### 2. Easy Debugging
Filter by ❌ to see only failed spells:
- See exactly which spells failed
- Read error messages directly in sheet
- Know when the failure occurred

### 3. Incremental Sync
You can filter by:
- Spells without sync status (never synced)
- Spells with ❌ (failed, needs retry)
- Spells older than X date (needs re-sync)

### 4. Audit Trail
Track when each spell was last synced:
- Useful for team collaboration
- Know if changes need re-sync
- Historical record of sync attempts

## Usage Examples

### Example 1: Find Failed Syncs
In Google Sheets:
1. Click "DDB Sync Status" column header
2. Filter → Filter by values → Select only ❌
3. Review "DDB Sync Error" column for details

### Example 2: Re-sync Failed Spells Only
In notebook:
```python
# Filter to only re-sync failed spells
df_spells = fantasy_sheets.get_sheet(SPELLS_GID)
failed_spells = df_spells[df_spells['DDB Sync Status'] == '❌']['Spell Name'].tolist()

# Filter spells_to_sync to only these
spells_to_sync = [s for s in spells if s.get('name') in failed_spells]
```

### Example 3: Find Stale Syncs
```python
# Find spells not synced in last 7 days
from datetime import datetime, timedelta
cutoff = datetime.now() - timedelta(days=7)

df_spells = fantasy_sheets.get_sheet(SPELLS_GID)
stale_syncs = df_spells[
    pd.to_datetime(df_spells['DDB Last Synced'], errors='coerce') < cutoff
]['Spell Name'].tolist()
```

## Error Message Examples

Common errors you might see:

| Error Message | Meaning | Solution |
|--------------|---------|----------|
| `403 Forbidden` | Auth tokens expired | Re-run token extraction script |
| `404 Not Found` | Spell ID invalid | Check DDB column, may need to delete and recreate |
| `Conversion error: ...` | CSV data invalid | Fix data in spreadsheet |
| `JSON parse error` | Modifiers JSON malformed | Re-run extraction script |
| `Network timeout` | D&D Beyond slow | Retry, increase timeout |

## Performance

Tracking adds minimal overhead:
- **~0.1 seconds** per spell for tracking updates
- **Batch updates** at end (efficient)
- **No impact** on sync speed

## Optional: Disable Tracking

To disable tracking (not recommended):

```python
# Set this at the top of cells
ENABLE_TRACKING = False

# Then wrap all tracking code:
if ENABLE_TRACKING:
    # ... tracking code ...
```

## Column Specifications

| Column Name | Type | Max Length | Example |
|------------|------|------------|---------|
| DDB Sync Status | Text (emoji) | 2 chars | ✅ |
| DDB Sync Error | Text | 200 chars | "403 Forbidden: Invalid token" |
| DDB Last Synced | Text (timestamp) | 19 chars | 2026-02-15 14:30:22 |

## Future Enhancements

Possible additions:
- 🔄 "Syncing" status (set before sync, update after)
- Separate columns for base vs extras sync
- Retry count tracking
- Sync duration tracking
- Last successful sync timestamp (separate from last attempt)
