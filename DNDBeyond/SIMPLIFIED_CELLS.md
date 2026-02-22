# Simplified Notebook Cells

Replace Cell 13 and Cell 14 with these much shorter versions:

## Cell 13 (Base Spell Sync) - SIMPLIFIED

```python
# ============================================
# SYNC SPELLS (SIMPLIFIED)
# ============================================

from DNDBeyond.helpers.sync import SpellSyncManager
from DNDBeyond.helpers import convert_spell_to_ddb, normalize_ddb_id

# Configuration
DRY_RUN = False
BATCH_SIZE = None  # None for all, or number to limit
SKIP_EXISTING = False
UPDATE_EXISTING = True
UPDATE_ADDITIONAL_FIELDS = True
VERBOSE = True

# Create sync manager
sync_manager = SpellSyncManager(
    ddb_api=ddb_api,
    fantasy_sheets=fantasy_sheets,
    spells_gid=SPELLS_GID,
    delay=1
)

# Run sync
results = sync_manager.sync_base_spells(
    spells=spells,
    converter_func=convert_spell_to_ddb,
    normalize_ddb_id_func=normalize_ddb_id,
    dry_run=DRY_RUN,
    batch_size=BATCH_SIZE,
    skip_existing=SKIP_EXISTING,
    update_existing=UPDATE_EXISTING,
    update_additional_fields=UPDATE_ADDITIONAL_FIELDS,
    verbose=VERBOSE
)

print(f"\n✓ Sync complete: {results['created']} created, {results['updated']} updated, {results['errors']} errors")
```

## Cell 14 (Extras Sync) - SIMPLIFIED

```python
# ============================================
# SYNC CONDITIONS, MODIFIERS & HIGHER LEVELS (SIMPLIFIED)
# ============================================

from DNDBeyond.helpers.sync import SpellSyncManager
from DNDBeyond.helpers import (
    extract_spell_conditions,
    extract_spell_modifiers,
    extract_spell_scaling,
    parse_dice_scaling,
    normalize_ddb_id
)

# Configuration
SYNC_CONDITIONS = True
SYNC_MODIFIERS = True
SYNC_HIGHER_LEVELS = True
ONLY_NEW_SPELLS = False
DRY_RUN_EXTRAS = False
CLEAN_UPDATE = True

# Create sync manager
sync_manager = SpellSyncManager(
    ddb_api=ddb_api,
    fantasy_sheets=fantasy_sheets,
    spells_gid=SPELLS_GID,
    delay=1
)

# Run extras sync
stats = sync_manager.sync_extras(
    spells=spells,
    extract_conditions_func=extract_spell_conditions,
    extract_modifiers_func=extract_spell_modifiers,
    extract_scaling_func=extract_spell_scaling,
    parse_scaling_func=parse_dice_scaling,
    normalize_ddb_id_func=normalize_ddb_id,
    sync_conditions=SYNC_CONDITIONS,
    sync_modifiers=SYNC_MODIFIERS,
    sync_higher_levels=SYNC_HIGHER_LEVELS,
    only_new_spells=ONLY_NEW_SPELLS,
    dry_run=DRY_RUN_EXTRAS,
    clean_update=CLEAN_UPDATE
)

print(f"\n✓ Extras sync complete: {stats['modifiers_created']} modifiers, {stats['conditions_created']} conditions, {stats['higher_levels_created']} higher levels")
```

## Benefits

**Before:** ~300 lines per cell, laggy notebook
**After:** ~30 lines per cell, much faster

All the complex logic is now in `/DNDBeyond/helpers/sync.py` which:
- ✅ Is easier to maintain and test
- ✅ Has better error handling
- ✅ Can be reused across notebooks
- ✅ Doesn't slow down the notebook UI
- ✅ Shows detailed error messages from D&D Beyond

The notebook cells are now just configuration + a simple function call!
