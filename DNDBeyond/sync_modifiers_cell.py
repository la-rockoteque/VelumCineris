# ============================================
# SYNC CONDITIONS, HIGHER LEVELS, AND MODIFIERS
# ============================================

from DNDBeyond.helpers import (
    extract_spell_conditions,
    extract_spell_modifiers,  # NEW!
    extract_spell_scaling,
    parse_dice_scaling
)

SYNC_CONDITIONS = True  # Set to False to skip condition creation
SYNC_MODIFIERS = True  # NEW! Set to False to skip modifier creation
SYNC_HIGHER_LEVELS = False  # Set to True to create structured higher level scaling
ONLY_NEW_SPELLS = False  # Set to True to only process newly created spells
DRY_RUN_EXTRAS = False  # Set to False to actually create conditions/modifiers/scaling

print("=" * 60)
print("SYNC CONDITIONS, MODIFIERS & HIGHER LEVELS")
print("=" * 60)
if DRY_RUN_EXTRAS:
    print("DRY RUN - Nothing will be created")
else:
    print("⚠️  LIVE MODE - Conditions/modifiers/scaling WILL be created!")
print(f"Sync Conditions: {'YES' if SYNC_CONDITIONS else 'NO'}")
print(f"Sync Modifiers: {'YES' if SYNC_MODIFIERS else 'NO'}")  # NEW!
print(f"Sync Higher Levels: {'YES' if SYNC_HIGHER_LEVELS else 'NO'}")
print(f"Only New Spells: {'YES' if ONLY_NEW_SPELLS else 'NO'}")
print("=" * 60)
print()

if not SYNC_CONDITIONS and not SYNC_MODIFIERS and not SYNC_HIGHER_LEVELS:
    print("⚠️  All sync options are False")
    print("   Nothing to do. Enable at least one to proceed.")
else:
    # Get spells with DDB IDs
    df_spells = fantasy_sheets.get_sheet(SPELLS_GID)
    spell_data_map = {}

    # Build a map of spell name → (spell dict, ddb_id)
    for spell in spells:
        spell_name = spell.get("name")
        if spell_name:
            # Get DDB ID from spreadsheet
            df_row = df_spells[df_spells['Spell Name'] == spell_name]
            if not df_row.empty:
                ddb_id = normalize_ddb_id(df_row.iloc[0].get('DDB'))
                if ddb_id:
                    spell_data_map[spell_name] = (spell, ddb_id)

    print(f"Found {len(spell_data_map)} spells with DDB IDs")
    print()

    # Filter to only newly created spells if requested
    if ONLY_NEW_SPELLS and 'results' in dir():
        created_names = [d['title'] for d in results.get('details', []) if d.get('action') == 'created']
        spell_data_map = {k: v for k, v in spell_data_map.items() if k in created_names}
        print(f"Filtered to {len(spell_data_map)} newly created spells")
        print()

    if not spell_data_map:
        print("⚠️  No spells to process")
    else:
        conditions_created = 0
        modifiers_created = 0  # NEW!
        higher_levels_created = 0
        errors = 0

        for i, (spell_name, (spell, ddb_id)) in enumerate(spell_data_map.items(), 1):
            print(f"[{i}/{len(spell_data_map)}] Processing: {spell_name} (ID: {ddb_id})")

            try:
                # Process conditions
                if SYNC_CONDITIONS:
                    conditions = extract_spell_conditions(spell)
                    if conditions:
                        print(f"  → Found {len(conditions)} condition(s) to add")
                        for condition_data in conditions:
                            if DRY_RUN_EXTRAS:
                                print(f"    DRY RUN: Would create condition: {condition_data['condition']}")
                            else:
                                success = ddb_api.create_condition(ddb_id, condition_data)
                                if success:
                                    print(f"    ✓ Created condition")
                                    conditions_created += 1
                                else:
                                    print(f"    ✗ Failed to create condition")
                                    errors += 1
                                time.sleep(DELAY)

                # NEW! Process modifiers
                if SYNC_MODIFIERS:
                    modifiers = extract_spell_modifiers(spell)
                    if modifiers:
                        print(f"  → Found {len(modifiers)} modifier(s) to add")
                        for modifier_data in modifiers:
                            if DRY_RUN_EXTRAS:
                                type_names = ["", "AC", "Attack", "Damage", "Save", "Ability Check",
                                             "Skill", "Speed", "Initiative", "HP", "Temp HP"]
                                type_idx = int(modifier_data.get('type', 0))
                                type_name = type_names[type_idx] if type_idx < len(type_names) else "Unknown"
                                print(f"    DRY RUN: Would create {type_name} modifier")
                            else:
                                success = ddb_api.create_modifier(ddb_id, modifier_data)
                                if success:
                                    print(f"    ✓ Created modifier")
                                    modifiers_created += 1
                                else:
                                    print(f"    ✗ Failed to create modifier")
                                    errors += 1
                                time.sleep(DELAY)

                # Process higher level scaling
                if SYNC_HIGHER_LEVELS:
                    scaling_text = extract_spell_scaling(spell)
                    if scaling_text:
                        higher_levels = parse_dice_scaling(scaling_text)
                        if higher_levels:
                            print(f"  → Found {len(higher_levels)} higher level scaling entr(ies)")
                            for level_data in higher_levels:
                                if DRY_RUN_EXTRAS:
                                    print(f"    DRY RUN: Would create scaling at level {level_data['level']}")
                                else:
                                    success = ddb_api.create_higher_level(ddb_id, level_data)
                                    if success:
                                        print(f"    ✓ Created higher level scaling")
                                        higher_levels_created += 1
                                    else:
                                        print(f"    ✗ Failed to create higher level scaling")
                                        errors += 1
                                    time.sleep(DELAY)

            except Exception as e:
                print(f"  ✗ Error processing spell: {e}")
                errors += 1

        print()
        print("=" * 60)
        print("EXTRAS SYNC COMPLETE")
        print("=" * 60)
        if DRY_RUN_EXTRAS:
            print(f"DRY RUN: Would create {conditions_created} conditions")
            print(f"DRY RUN: Would create {modifiers_created} modifiers")  # NEW!
            print(f"DRY RUN: Would create {higher_levels_created} higher level entries")
        else:
            print(f"✓ Conditions created: {conditions_created}")
            print(f"✓ Modifiers created: {modifiers_created}")  # NEW!
            print(f"✓ Higher levels created: {higher_levels_created}")
            print(f"✗ Errors: {errors}")
        print("=" * 60)
