"""Spell sync manager for D&D Beyond."""

import time
from datetime import datetime
from typing import Dict, List, Optional
import pandas as pd


class SpellSyncManager:
    """Manages syncing spells to D&D Beyond."""

    def __init__(self, ddb_api, fantasy_sheets, spells_gid: str, delay: float = 1.0):
        self.ddb_api = ddb_api
        self.fantasy_sheets = fantasy_sheets
        self.spells_gid = spells_gid
        self.delay = delay

    def sync_base_spells(
        self,
        spells: List[Dict],
        converter_func,
        normalize_ddb_id_func,
        dry_run: bool = False,
        batch_size: Optional[int] = None,
        skip_existing: bool = False,
        update_existing: bool = True,
        update_additional_fields: bool = True,
        verbose: bool = True,
    ) -> Dict:
        """Sync base spell information (create/update spells).

        Args:
            spells: List of spell dicts from 5etools format
            converter_func: Function to convert spell to DDB format
            normalize_ddb_id_func: Function to normalize DDB IDs
            dry_run: If True, don't actually make changes
            batch_size: Limit number of spells to process
            skip_existing: Skip spells that already have DDB IDs
            update_existing: Update spells when DDB ID exists
            update_additional_fields: Update AOE/save/attack after creation
            verbose: Print detailed logging

        Returns:
            Dict with sync results
        """
        from DNDBeyond.core.Helpers.DnDBeyondAPI import DnDBeyondAPI

        print("=" * 60)
        if dry_run:
            print("DRY RUN - No spells will be created/updated")
        else:
            print("⚠️  LIVE MODE - Spells WILL be created/updated!")
        print("=" * 60)
        print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Batch size: {'ALL SPELLS' if batch_size is None else batch_size}")
        print(f"Skip existing: {'YES' if skip_existing else 'NO'}")
        print(f"Update existing: {'YES' if update_existing else 'NO'}")
        print()

        # Ensure tracking columns exist
        self._ensure_tracking_columns()

        # Select spells to sync
        spells_to_sync = spells if batch_size is None else spells[:batch_size]
        print(f"Total spells to process: {len(spells_to_sync)}")
        print()

        # Get existing DDB IDs from spreadsheet
        spell_to_ddb_id = self._load_existing_ddb_ids(normalize_ddb_id_func)
        print(f"✓ Found {len(spell_to_ddb_id)} spells with DDB IDs in spreadsheet")

        # Fetch existing spells from D&D Beyond
        existing_spells = []
        if not dry_run:
            try:
                existing_spells = self.ddb_api.get_user_spells()
                print(f"✓ Found {len(existing_spells)} existing homebrew spells\n")
            except Exception as e:
                print(f"⚠️  Could not fetch existing spells: {e}\n")

        results = {
            "created": 0,
            "updated": 0,
            "skipped": 0,
            "errors": 0,
            "details": [],
        }

        spreadsheet_updates = []
        sync_tracking_updates = []

        for i, spell in enumerate(spells_to_sync, 1):
            spell_name = spell.get("name", "Unnamed")
            print(f"[{i}/{len(spells_to_sync)}] Processing: {spell_name}")

            try:
                # Convert to D&D Beyond format
                if verbose:
                    print(f"  → Converting spell to D&D Beyond format...")

                ddb_data = converter_func(spell)

                # Check if spell already has DDB ID
                existing_id = spell_to_ddb_id.get(spell_name)

                if existing_id:
                    # Spell has a DDB ID
                    if update_existing and not skip_existing:
                        # UPDATE mode
                        if dry_run:
                            print(f"  → DRY RUN: Would update spell (ID: {existing_id})")
                            results["updated"] += 1
                        else:
                            print(f"  → Updating existing spell (ID: {existing_id})")
                            slug = DnDBeyondAPI.create_slug(spell_name)
                            updated = self.ddb_api.update_basic_information(
                                existing_id, slug, ddb_data
                            )

                            if updated:
                                print(f"  ✓ Updated spell successfully")
                                results["updated"] += 1
                            else:
                                print(f"  ✗ Failed to update spell")
                                error_msg = (
                                    str(self.ddb_api.last_error)
                                    if self.ddb_api.last_error
                                    else "Update failed"
                                )
                                results["errors"] += 1
                                sync_tracking_updates.append(
                                    {
                                        "spell_name": spell_name,
                                        "status": "❌",
                                        "error": error_msg[:200],
                                        "timestamp": datetime.now().strftime(
                                            "%Y-%m-%d %H:%M:%S"
                                        ),
                                    }
                                )
                                continue

                            time.sleep(self.delay)

                        sync_tracking_updates.append(
                            {
                                "spell_name": spell_name,
                                "status": "✅",
                                "error": "",
                                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            }
                        )
                    else:
                        # SKIP mode
                        print(f"  ✓ Already synced (DDB ID: {existing_id})")
                        results["skipped"] += 1

                    continue

                # No existing ID - CREATE new spell
                if dry_run:
                    print(f"  → DRY RUN: Would create spell")
                    results["created"] += 1
                    sync_tracking_updates.append(
                        {
                            "spell_name": spell_name,
                            "status": "✅",
                            "error": "",
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        }
                    )
                else:
                    if verbose:
                        print(f"  → Creating spell on D&D Beyond...")

                    spell_id = self.ddb_api.create_spell(ddb_data)

                    if spell_id:
                        print(f"  ✓ Created: ID {spell_id}")

                        # Update additional fields if enabled
                        if update_additional_fields:
                            slug = DnDBeyondAPI.create_slug(spell_name)
                            self.ddb_api.update_basic_information(
                                spell_id, slug, ddb_data
                            )

                        spreadsheet_updates.append(
                            {
                                "match_value": spell_name,
                                "update_column": "DDB",
                                "update_value": spell_id,
                            }
                        )

                        results["created"] += 1
                        sync_tracking_updates.append(
                            {
                                "spell_name": spell_name,
                                "status": "✅",
                                "error": "",
                                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            }
                        )
                    else:
                        print(f"  ✗ Failed to create spell")
                        error_msg = (
                            str(self.ddb_api.last_error)
                            if self.ddb_api.last_error
                            else "Unknown error"
                        )
                        results["errors"] += 1
                        sync_tracking_updates.append(
                            {
                                "spell_name": spell_name,
                                "status": "❌",
                                "error": error_msg[:200],
                                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            }
                        )

                    time.sleep(self.delay)

            except Exception as e:
                print(f"  ✗ Unexpected error: {e}")
                results["errors"] += 1
                sync_tracking_updates.append(
                    {
                        "spell_name": spell_name,
                        "status": "❌",
                        "error": str(e)[:200],
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    }
                )

        # Update spreadsheet
        if not dry_run:
            self._update_tracking_columns(sync_tracking_updates)
            self._update_ddb_ids(spreadsheet_updates)

        # Print summary
        self._print_sync_summary(results, dry_run)

        return results

    def sync_extras(
        self,
        spells: List[Dict],
        extract_conditions_func,
        extract_modifiers_func,
        extract_scaling_func,
        parse_scaling_func,
        normalize_ddb_id_func,
        sync_conditions: bool = True,
        sync_modifiers: bool = True,
        sync_higher_levels: bool = True,
        only_new_spells: bool = False,
        dry_run: bool = False,
        clean_update: bool = True,
    ) -> Dict:
        """Sync spell extras (modifiers, conditions, higher levels).

        Args:
            spells: List of spell dicts
            extract_conditions_func: Function to extract conditions
            extract_modifiers_func: Function to extract modifiers
            extract_scaling_func: Function to extract scaling text
            parse_scaling_func: Function to parse scaling to entries
            normalize_ddb_id_func: Function to normalize DDB IDs
            sync_conditions: Whether to sync conditions
            sync_modifiers: Whether to sync modifiers
            sync_higher_levels: Whether to sync higher level scaling
            only_new_spells: Only process newly created spells
            dry_run: If True, don't make changes
            clean_update: Delete existing before creating new

        Returns:
            Dict with sync results
        """
        from DNDBeyond.core.Helpers.DnDBeyondAPI import DnDBeyondAPI

        print("=" * 60)
        print("SYNC CONDITIONS, MODIFIERS & HIGHER LEVELS")
        print("=" * 60)
        if dry_run:
            print("DRY RUN - Nothing will be created/deleted")
        else:
            print("⚠️  LIVE MODE - Changes WILL be made!")
        print(f"Sync Conditions: {'YES' if sync_conditions else 'NO'}")
        print(f"Sync Modifiers: {'YES' if sync_modifiers else 'NO'}")
        print(f"Sync Higher Levels: {'YES' if sync_higher_levels else 'NO'}")
        print(f"Clean Update: {'YES' if clean_update else 'NO'}")
        print("=" * 60)
        print()

        if not any([sync_conditions, sync_modifiers, sync_higher_levels]):
            print("⚠️  All sync options are False - nothing to do")
            return {}

        # Get spells with DDB IDs
        spell_data_map = self._build_spell_data_map(spells, normalize_ddb_id_func)
        print(f"Found {len(spell_data_map)} spells with DDB IDs")
        print()

        if not spell_data_map:
            print("⚠️  No spells to process")
            return {}

        stats = {
            "conditions_created": 0,
            "conditions_deleted": 0,
            "modifiers_created": 0,
            "modifiers_deleted": 0,
            "higher_levels_created": 0,
            "higher_levels_deleted": 0,
            "errors": 0,
        }

        extras_tracking_updates = []

        for i, (spell_name, (spell, ddb_id)) in enumerate(spell_data_map.items(), 1):
            print(f"[{i}/{len(spell_data_map)}] Processing: {spell_name} (ID: {ddb_id})")

            try:
                spell_had_error = False
                spell_error_msg = ""

                # Get existing extras if doing clean update
                existing_extras = None
                if clean_update and not dry_run:
                    slug = DnDBeyondAPI.create_slug(spell_name)
                    existing_extras = self.ddb_api.get_spell_extras(ddb_id, slug)

                # Process conditions
                if sync_conditions:
                    result = self._process_conditions(
                        spell,
                        ddb_id,
                        extract_conditions_func,
                        existing_extras,
                        clean_update,
                        dry_run,
                    )
                    stats["conditions_created"] += result["created"]
                    stats["conditions_deleted"] += result["deleted"]
                    if result["error"]:
                        spell_had_error = True
                        spell_error_msg = result["error"]

                # Process modifiers
                if sync_modifiers:
                    result = self._process_modifiers(
                        spell,
                        ddb_id,
                        extract_modifiers_func,
                        existing_extras,
                        clean_update,
                        dry_run,
                    )
                    stats["modifiers_created"] += result["created"]
                    stats["modifiers_deleted"] += result["deleted"]
                    if result["error"]:
                        spell_had_error = True
                        spell_error_msg = result["error"]

                # Process higher levels
                if sync_higher_levels:
                    result = self._process_higher_levels(
                        spell,
                        ddb_id,
                        extract_scaling_func,
                        parse_scaling_func,
                        existing_extras,
                        clean_update,
                        dry_run,
                    )
                    stats["higher_levels_created"] += result["created"]
                    stats["higher_levels_deleted"] += result["deleted"]
                    if result["error"]:
                        spell_had_error = True
                        spell_error_msg = result["error"]

                # Track status
                extras_tracking_updates.append(
                    {
                        "spell_name": spell_name,
                        "status": "❌" if spell_had_error else "✅",
                        "error": spell_error_msg[:180] if spell_had_error else "",
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    }
                )

            except Exception as e:
                print(f"  ✗ Error processing spell: {e}")
                stats["errors"] += 1
                extras_tracking_updates.append(
                    {
                        "spell_name": spell_name,
                        "status": "❌",
                        "error": f"Extras sync failed: {str(e)[:180]}",
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    }
                )

        # Update spreadsheet
        if not dry_run:
            self._update_tracking_columns(extras_tracking_updates)

        # Print summary
        print()
        print("=" * 60)
        print("EXTRAS SYNC COMPLETE")
        print("=" * 60)
        if dry_run:
            print(
                f"DRY RUN: Would delete {stats['modifiers_deleted']} modifiers, "
                f"{stats['conditions_deleted']} conditions, {stats['higher_levels_deleted']} higher levels"
            )
            print(
                f"DRY RUN: Would create {stats['modifiers_created']} modifiers, "
                f"{stats['conditions_created']} conditions, {stats['higher_levels_created']} higher levels"
            )
        else:
            if clean_update:
                print(
                    f"✓ Deleted: {stats['modifiers_deleted']} modifiers, "
                    f"{stats['conditions_deleted']} conditions, {stats['higher_levels_deleted']} higher levels"
                )
            print(
                f"✓ Created: {stats['modifiers_created']} modifiers, "
                f"{stats['conditions_created']} conditions, {stats['higher_levels_created']} higher levels"
            )
            print(f"✗ Errors: {stats['errors']}")
        print("=" * 60)

        return stats

    def _ensure_tracking_columns(self):
        """Ensure sync tracking columns exist."""
        for col_name in ["DDB Sync Status", "DDB Sync Error", "DDB Last Synced"]:
            try:
                self.fantasy_sheets.ensure_column_exists(self.spells_gid, col_name)
            except Exception:
                pass

    def _load_existing_ddb_ids(self, normalize_func) -> Dict[str, str]:
        """Load existing DDB IDs from spreadsheet."""
        df = self.fantasy_sheets.get_sheet(self.spells_gid)
        spell_to_ddb_id = {}

        if "DDB" in df.columns and "Spell Name" in df.columns:
            for _, row in df.iterrows():
                spell_name = row.get("Spell Name")
                ddb_id = row.get("DDB")
                if spell_name and pd.notna(ddb_id):
                    normalized_id = normalize_func(ddb_id)
                    if normalized_id:
                        spell_to_ddb_id[spell_name] = normalized_id

        return spell_to_ddb_id

    def _build_spell_data_map(self, spells: List[Dict], normalize_func) -> Dict:
        """Build map of spell name to (spell dict, ddb_id)."""
        df = self.fantasy_sheets.get_sheet(self.spells_gid)
        spell_data_map = {}

        for spell in spells:
            spell_name = spell.get("name")
            if spell_name:
                df_row = df[df["Spell Name"] == spell_name]
                if not df_row.empty:
                    ddb_id = normalize_func(df_row.iloc[0].get("DDB"))
                    if ddb_id:
                        spell_data_map[spell_name] = (spell, ddb_id)

        return spell_data_map

    def _process_conditions(
        self, spell, ddb_id, extract_func, existing_extras, clean_update, dry_run
    ):
        """Process conditions for a spell."""
        result = {"created": 0, "deleted": 0, "error": ""}
        conditions = extract_func(spell)

        # Delete existing if clean update
        if clean_update and existing_extras and existing_extras.get("conditions"):
            for cond in existing_extras["conditions"]:
                if not dry_run:
                    if self.ddb_api.delete_condition(ddb_id, cond["id"]):
                        result["deleted"] += 1
                    time.sleep(self.delay)

        # Create new conditions
        if conditions:
            print(f"  → Adding {len(conditions)} condition(s)")
            for condition_data in conditions:
                if not dry_run:
                    if self.ddb_api.create_condition(ddb_id, condition_data):
                        print(f"    ✓ Created condition")
                        result["created"] += 1
                    else:
                        error_detail = self._get_error_detail()
                        print(f"    ✗ Failed to create condition: {error_detail}")
                        result["error"] = f"Failed to create condition: {error_detail}"
                    time.sleep(self.delay)

        return result

    def _process_modifiers(
        self, spell, ddb_id, extract_func, existing_extras, clean_update, dry_run
    ):
        """Process modifiers for a spell."""
        result = {"created": 0, "deleted": 0, "error": ""}
        modifiers = extract_func(spell)

        # Delete existing if clean update
        if clean_update and existing_extras and existing_extras.get("modifiers"):
            for mod in existing_extras["modifiers"]:
                if not dry_run:
                    if self.ddb_api.delete_modifier(ddb_id, mod["id"]):
                        result["deleted"] += 1
                    time.sleep(self.delay)

        # Create new modifiers
        if modifiers:
            print(f"  → Adding {len(modifiers)} modifier(s)")
            for modifier_data in modifiers:
                if not dry_run:
                    if self.ddb_api.create_modifier(ddb_id, modifier_data):
                        print(f"    ✓ Created modifier")
                        result["created"] += 1
                    else:
                        error_detail = self._get_error_detail()
                        print(f"    ✗ Failed to create modifier: {error_detail}")
                        result["error"] = f"Failed to create modifier: {error_detail}"
                    time.sleep(self.delay)

        return result

    def _process_higher_levels(
        self,
        spell,
        ddb_id,
        extract_func,
        parse_func,
        existing_extras,
        clean_update,
        dry_run,
    ):
        """Process higher level scaling for a spell."""
        result = {"created": 0, "deleted": 0, "error": ""}
        scaling_text = extract_func(spell)

        if not scaling_text:
            return result

        higher_levels = parse_func(scaling_text)

        # Delete existing if clean update
        if clean_update and existing_extras and existing_extras.get("higher_levels"):
            for hl in existing_extras["higher_levels"]:
                if not dry_run:
                    if self.ddb_api.delete_higher_level(ddb_id, hl["id"]):
                        result["deleted"] += 1
                    time.sleep(self.delay)

        # Create new higher levels
        if higher_levels:
            print(f"  → Adding {len(higher_levels)} higher level entr(ies)")
            for level_data in higher_levels:
                if not dry_run:
                    if self.ddb_api.create_higher_level(ddb_id, level_data):
                        print(f"    ✓ Created higher level scaling")
                        result["created"] += 1
                    else:
                        error_detail = self._get_error_detail()
                        print(f"    ✗ Failed to create higher level: {error_detail}")
                        result["error"] = f"Failed to create higher level: {error_detail}"
                    time.sleep(self.delay)

        return result

    def _get_error_detail(self) -> str:
        """Get detailed error from last API call."""
        if self.ddb_api.last_error:
            if isinstance(self.ddb_api.last_error, dict):
                if "status_code" in self.ddb_api.last_error:
                    detail = f"HTTP {self.ddb_api.last_error['status_code']}: {self.ddb_api.last_error.get('reason', 'Unknown')}"
                    if self.ddb_api.last_error.get("response_preview"):
                        detail += f" | {self.ddb_api.last_error['response_preview'][:200]}"
                    return detail
                elif "exception_type" in self.ddb_api.last_error:
                    return f"{self.ddb_api.last_error['exception_type']}: {self.ddb_api.last_error.get('exception_message', 'Unknown')}"
            return str(self.ddb_api.last_error)
        return "Unknown error"

    def _update_tracking_columns(self, tracking_updates: List[Dict]):
        """Update sync tracking columns in spreadsheet."""
        if not tracking_updates:
            return

        print("\n" + "=" * 60)
        print("Updating sync status in Google Sheets...")
        print("=" * 60)

        status_updates = []
        error_updates = []
        timestamp_updates = []

        for tracking in tracking_updates:
            spell_name = tracking["spell_name"]
            status_updates.append(
                {
                    "match_value": spell_name,
                    "update_column": "DDB Sync Status",
                    "update_value": tracking["status"],
                }
            )
            error_updates.append(
                {
                    "match_value": spell_name,
                    "update_column": "DDB Sync Error",
                    "update_value": tracking["error"],
                }
            )
            timestamp_updates.append(
                {
                    "match_value": spell_name,
                    "update_column": "DDB Last Synced",
                    "update_value": tracking["timestamp"],
                }
            )

        try:
            self.fantasy_sheets.batch_update_cells_by_row_match(
                self.spells_gid, "Spell Name", status_updates
            )
            self.fantasy_sheets.batch_update_cells_by_row_match(
                self.spells_gid, "Spell Name", error_updates
            )
            self.fantasy_sheets.batch_update_cells_by_row_match(
                self.spells_gid, "Spell Name", timestamp_updates
            )
            print(f"✓ Updated sync status for {len(tracking_updates)} spells")
        except Exception as e:
            print(f"✗ Error updating tracking columns: {e}")

    def _update_ddb_ids(self, spreadsheet_updates: List[Dict]):
        """Update DDB IDs in spreadsheet."""
        if not spreadsheet_updates:
            return

        print("\n" + "=" * 60)
        print("Updating Google Sheets with DDB IDs...")
        print("=" * 60)

        try:
            update_results = self.fantasy_sheets.batch_update_cells_by_row_match(
                self.spells_gid, "Spell Name", spreadsheet_updates
            )
            success_count = sum(1 for v in update_results.values() if v)
            print(
                f"✓ Updated {success_count}/{len(spreadsheet_updates)} spells in spreadsheet"
            )

            failed = [k for k, v in update_results.items() if not v]
            if failed:
                print(f"⚠️  Failed to update {len(failed)} spells:")
                for spell_name in failed[:5]:
                    print(f"  - {spell_name}")
                if len(failed) > 5:
                    print(f"  ... and {len(failed) - 5} more")
        except Exception as e:
            print(f"✗ Error updating spreadsheet: {e}")

    def _print_sync_summary(self, results: Dict, dry_run: bool):
        """Print sync summary."""
        print()
        print("=" * 60)
        print("SYNC COMPLETE")
        print("=" * 60)
        if dry_run:
            print(f"DRY RUN: Would create {results['created']} spells")
            print(f"DRY RUN: Would update {results['updated']} spells")
        else:
            print(f"✓ Created: {results['created']}")
            print(f"✓ Updated: {results['updated']}")
            print(f"⚠️  Skipped: {results['skipped']}")
            print(f"✗ Errors: {results['errors']}")
        print("=" * 60)
        print(f"End time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
