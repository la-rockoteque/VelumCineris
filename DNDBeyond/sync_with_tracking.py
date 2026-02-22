# Helper functions for sync tracking
# Add these at the top of your notebook cells

from datetime import datetime

def update_sync_status(spell_name, status_emoji, error_msg="", timestamp=None):
    """Track sync status in spreadsheet.

    Args:
        spell_name: Name of the spell
        status_emoji: ✅ (success), ❌ (failed), 🔄 (in progress)
        error_msg: Error message if failed
        timestamp: Sync timestamp (defaults to now)
    """
    if timestamp is None:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    updates = [
        {
            'match_value': spell_name,
            'update_column': 'DDB Sync Status',
            'update_value': status_emoji
        },
        {
            'match_value': spell_name,
            'update_column': 'DDB Sync Error',
            'update_value': error_msg
        },
        {
            'match_value': spell_name,
            'update_column': 'DDB Last Synced',
            'update_value': timestamp
        }
    ]

    return updates

# Ensure tracking columns exist
def ensure_tracking_columns():
    """Ensure sync tracking columns exist in spreadsheet."""
    for col_name in ['DDB Sync Status', 'DDB Sync Error', 'DDB Last Synced']:
        try:
            fantasy_sheets.ensure_column_exists(SPELLS_GID, col_name)
        except Exception as e:
            print(f"  ⚠️  Could not ensure column '{col_name}': {e}")
