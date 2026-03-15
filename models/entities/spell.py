"""
Spell entity model for D&D 5e.

Provides type-safe validation for spell data from Google Sheets.
"""

import json
import re
import urllib.parse
from typing import Any, Dict, List, Literal, Optional

import inflection
from pydantic import Field

from ..base import BaseEntity
from ..fields.components import Components, TimeAction, Range, Duration, Distance
from ..row_access import is_missing as row_is_missing, optional_int, optional_text, row_value

# Valid spell schools (5etools format)
SchoolType = Literal["A", "C", "D", "E", "V", "I", "N", "T"]


def _is_missing(value: Any) -> bool:
    return row_is_missing(value)


def _optional_text(value: Any) -> Optional[str]:
    if _is_missing(value):
        return None
    text = str(value).strip()
    return text if text else None


def _split_csv(value: Any, *, lower: bool = False) -> Optional[List[str]]:
    text = _optional_text(value)
    if not text:
        return None
    out: list[str] = []
    for chunk in text.split(","):
        item = chunk.strip()
        if not item:
            continue
        out.append(item.lower() if lower else item)
    return out or None


def _first_child_value(rows: list[dict[str, Any]], *keys: str) -> Optional[str]:
    for row in rows:
        for key in keys:
            value = _optional_text(row_value(row, key))
            if value:
                return value
    return None


def _collect_child_values(
    rows: list[dict[str, Any]],
    *keys: str,
    lower: bool = False,
    split_commas: bool = False,
) -> list[str]:
    values: list[str] = []
    for row in rows:
        for key in keys:
            text = _optional_text(row_value(row, key))
            if not text:
                continue
            parts = [text]
            if split_commas:
                parts = [part.strip() for part in text.split(",") if part.strip()]
            for part in parts:
                values.append(part.lower() if lower else part)
    deduped: list[str] = []
    seen: set[str] = set()
    for item in values:
        marker = item.strip().lower()
        if not marker or marker in seen:
            continue
        seen.add(marker)
        deduped.append(item.strip())
    return deduped


def _parse_bool(value: Any) -> bool:
    text = _optional_text(value)
    if not text:
        return False
    return text.strip().lower() in {"true", "1", "yes", "y"}


def _parse_int(value: Any, fallback: int) -> int:
    if _is_missing(value):
        return fallback
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    text = _optional_text(value)
    if not text:
        return fallback
    match = re.search(r"-?\d+", text)
    if not match:
        return fallback
    return int(match.group(0))


def _parse_level(value: Any) -> int:
    return max(0, min(9, _parse_int(value, 0)))


def _parse_school(row) -> SchoolType:
    school = _optional_text(row_value(row, "School ABRV")) or _optional_text(row_value(row, "School")) or "E"
    school_map = {
        "abjuration": "A",
        "conjuration": "C",
        "divination": "D",
        "enchantment": "E",
        "evocation": "V",
        "illusion": "I",
        "necromancy": "N",
        "transmutation": "T",
    }
    lowered = school.strip().lower()
    if lowered in school_map:
        return school_map[lowered]  # type: ignore[return-value]
    initial = school.strip()[:1].upper() or "E"
    if initial in {"A", "C", "D", "E", "V", "I", "N", "T"}:
        return initial  # type: ignore[return-value]
    return "E"


class Spell(BaseEntity):
    """
    D&D 5e Spell model.

    Represents a spell in 5etools JSON format.
    """

    # Core spell fields
    level: int = Field(..., ge=0, le=9, description="Spell level (0-9)")
    school: SchoolType = Field(..., description="Spell school abbreviation")
    components: Components = Field(..., description="Spell components (V, S, M, R)")
    time: List[TimeAction] = Field(..., description="Casting time")
    range: Range = Field(..., description="Spell range")
    duration: List[Duration] = Field(..., description="Spell duration")

    # Class associations
    classes: Optional[Dict[str, List[Dict[str, str]]]] = Field(
        None, description="Classes that can cast this spell"
    )

    # Higher level casting
    entriesHigherLevel: Optional[List[Dict[str, Any]]] = Field(
        None, description="Higher level casting effects"
    )

    # Optional 5etools tags
    abilityCheck: Optional[List[str]] = Field(None, description="Required ability checks")
    miscTags: Optional[List[str]] = Field(None, description="Miscellaneous tags")
    damageInflict: Optional[List[str]] = Field(None, description="Damage types inflicted")
    savingThrow: Optional[List[str]] = Field(None, description="Required saving throws")
    areaTags: Optional[List[str]] = Field(None, description="Area of effect tags")

    @classmethod
    def from_row(
        cls,
        row,
        source: str,
        json_source: str,
        *,
        modifiers_rows: Optional[List[Dict[str, Any]]] = None,
        scaling_rows: Optional[List[Dict[str, Any]]] = None,
        condition_rows: Optional[List[Dict[str, Any]]] = None,
    ) -> "Spell":
        """
        Create Spell from DataFrame row.

        Args:
            row: Row-like mapping from the sheet layer
            source: Source filter (e.g., "ORIO")
            json_source: JSON source identifier (e.g., "ORIO")
            modifiers_rows: Optional rows from Spells:Modifiers child sheet
            scaling_rows: Optional rows from Spells:Scaling child sheet
            condition_rows: Optional rows from Spells:Conditions child sheet

        Returns:
            Validated Spell instance
        """
        modifiers_rows = modifiers_rows or []
        scaling_rows = scaling_rows or []
        condition_rows = condition_rows or []

        spell_name = _optional_text(row_value(row, "Spell Name")) or _optional_text(row_value(row, "Name")) or "Unnamed Spell"

        # Parse components
        components_str = _optional_text(row_value(row, "Components ABVR")) or _optional_text(row_value(row, "Components")) or ""
        components = Components.from_string(components_str)

        # Parse spell classes
        spell_classes = [
            item.strip() for item in str(row_value(row, "Class", "")).split(",") if item.strip()
        ]

        # Parse optional list fields
        ability_checks = _split_csv(row_value(row, "Ability Check"), lower=True)
        misc_tags = _split_csv(row_value(row, "Tag ABRV"))
        damages = _split_csv(row_value(row, "Old Damage Type"), lower=True)
        areas = _split_csv(row_value(row, "Area ABRV"))

        saving_throws = _split_csv(row_value(row, "Saving Throw"), lower=True)
        if not saving_throws:
            saving_throws = _collect_child_values(
                condition_rows,
                "Saving Throw",
                lower=True,
                split_commas=True,
            ) or None

        # Parse time
        casting_unit = _parse_int(row_value(row, "Casting Unit"), 1)
        casting_type = (_optional_text(row_value(row, "Casting Type")) or "action").lower()
        time = [TimeAction(number=casting_unit, unit=casting_type)]

        # Parse range
        range_distance = (_optional_text(row_value(row, "Range Distance")) or "self").lower()
        range_obj = Range(
            type=(_optional_text(row_value(row, "Range Type")) or "point").lower(),
            distance=Distance(
                type=range_distance,
                amount=_parse_int(row_value(row, "Range Unit"), 0) if _optional_text(row_value(row, "Range Unit")) else None,
            ),
        )

        # Parse duration
        duration_type = (_optional_text(row_value(row, "Duration Type")) or "timed").lower()
        duration_unit = (_optional_text(row_value(row, "Duration Unit")) or "minutes").lower()
        duration_amount = _parse_int(row_value(row, "Duration Amount"), 1)

        duration_dict = {
            "type": duration_type,
        }
        if duration_type == "timed":
            duration_dict["duration"] = {
                "type": duration_unit,
                "amount": duration_amount,
                "upTo": _parse_bool(row_value(row, "Up To")),
            }
            duration_dict["concentration"] = _parse_bool(row_value(row, "Concentration"))

        duration = [Duration(**duration_dict)]

        # Parse entries
        entries: list[str] = []
        for field in ("Description", "Clarification", "Table"):
            value = _optional_text(row_value(row, field))
            if value:
                entries.append(value)
        if not entries:
            entries = [""]

        scaling_texts = _collect_child_values(
            scaling_rows,
            "Scaling",
            "Scaling Effect",
            "Scaling Modifier",
            split_commas=False,
        )
        scaling_text = "\n".join(scaling_texts) if scaling_texts else None

        # Parse entriesHigherLevel
        entriesHigherLevel = None
        higher_levels = _optional_text(row_value(row, "Higher Levels"))
        if higher_levels:
            entriesHigherLevel = [
                {
                    "type": "entries",
                    "name": "At Higher Levels",
                    "entries": [higher_levels],
                }
            ]
        elif scaling_text:
            entriesHigherLevel = [
                {
                    "type": "entries",
                    "name": "At Higher Levels",
                    "entries": [scaling_text],
                }
            ]

        # Parse fluff
        base_url = "https://raw.githubusercontent.com/la-rockoteque/Vestigium/refs/heads/main/images/Spell"
        fluff_entries: list[str] = []
        for field in ("Flavor", "Alternative Flavor", "Quotes"):
            value = _optional_text(row_value(row, field))
            if value:
                fluff_entries.append(value)

        fluff = {
            "entries": fluff_entries,
            "images": [
                {
                    "type": "image",
                    "href": {
                        "type": "external",
                        "url": f"{base_url}/{urllib.parse.quote(inflection.underscore(spell_name))}.png",
                    },
                }
            ],
        } if fluff_entries else None

        # Parse classes
        classes = {
            "fromClassList": [
                {"name": item, "source": json_source} for item in spell_classes
            ]
        } if spell_classes else None

        # Helper function for optional string fields
        def optional_str(field_name: str) -> Optional[str]:
            return _optional_text(row_value(row, field_name))

        condition_names = _collect_child_values(condition_rows, "Condition", split_commas=True)
        ddb_condition = optional_str("Condition") or (", ".join(condition_names) if condition_names else None)

        ddb_save_success = optional_str("Success") or _first_child_value(condition_rows, "Success")
        ddb_save_fail = optional_str("Fail") or _first_child_value(condition_rows, "Fail")
        ddb_scaling = optional_str("Scaling") or scaling_text

        modifier_payloads: list[dict[str, str]] = []
        for item in modifiers_rows:
            payload = {
                "type": _optional_text(row_value(item, "Modifier Type")) or "",
                "subtype": _optional_text(row_value(item, "Modifier Subtype")) or "",
                "dice_count": _optional_text(row_value(item, "Modifier Dice Count")) or "",
                "dice_type": _optional_text(row_value(item, "Modifier Dice Type")) or "",
                "fixed_value": _optional_text(row_value(item, "Modifier Fixed Value")) or "",
                "duration": _optional_text(row_value(item, "Modifier Duration")) or "",
                "duration_unit": _optional_text(row_value(item, "Modifier Duration Unit")) or "",
            }
            details = _optional_text(row_value(item, "Modifier Details"))
            use_primary_stat = _optional_text(row_value(item, "Modifier Use Primary Stat"))
            if details:
                payload["details"] = details
            if use_primary_stat:
                payload["use_primary_stat"] = use_primary_stat
            if any(value for value in payload.values()):
                modifier_payloads.append(payload)

        ddb_modifiers_json = optional_str("Modifiers JSON")
        if not ddb_modifiers_json and modifier_payloads:
            ddb_modifiers_json = json.dumps(modifier_payloads, ensure_ascii=False)

        ddb_modifier_type = optional_str("Modifier Type") or _first_child_value(modifiers_rows, "Modifier Type")
        ddb_modifier_subtype = optional_str("Modifier Subtype") or _first_child_value(modifiers_rows, "Modifier Subtype")
        ddb_modifier_dice_count = optional_str("Modifier Dice Count") or _first_child_value(modifiers_rows, "Modifier Dice Count")
        ddb_modifier_dice_type = optional_str("Modifier Dice Type") or _first_child_value(modifiers_rows, "Modifier Dice Type")
        ddb_modifier_fixed_value = optional_str("Modifier Fixed Value") or _first_child_value(modifiers_rows, "Modifier Fixed Value")
        ddb_modifier_duration = optional_str("Modifier Duration") or _first_child_value(modifiers_rows, "Modifier Duration")
        ddb_modifier_duration_unit = optional_str("Modifier Duration Unit") or _first_child_value(modifiers_rows, "Modifier Duration Unit")

        return cls(
            source=json_source,
            name=spell_name,
            level=_parse_level(row_value(row, "Level")),
            school=_parse_school(row),
            components=components,
            time=time,
            range=range_obj,
            duration=duration,
            classes=classes,
            entries=entries,
            entriesHigherLevel=entriesHigherLevel,
            fluff=fluff,
            abilityCheck=ability_checks,
            miscTags=misc_tags,
            damageInflict=damages,
            savingThrow=saving_throws,
            areaTags=areas,
            # Compatibility metadata remains supported as model extras for sync flows.
            ddb_save_success=ddb_save_success,
            ddb_save_fail=ddb_save_fail,
            ddb_area_type=optional_str("Area Type"),
            ddb_area_distance=optional_str("Area Distance"),
            ddb_damage=optional_str("Damage"),
            ddb_condition=ddb_condition,
            ddb_scaling=ddb_scaling,
            ddb_modifiers_json=ddb_modifiers_json,
            ddb_modifier_type=ddb_modifier_type,
            ddb_modifier_subtype=ddb_modifier_subtype,
            ddb_modifier_dice_count=ddb_modifier_dice_count,
            ddb_modifier_dice_type=ddb_modifier_dice_type,
            ddb_modifier_fixed_value=ddb_modifier_fixed_value,
            ddb_modifier_duration=ddb_modifier_duration,
            ddb_modifier_duration_unit=ddb_modifier_duration_unit,
        )
