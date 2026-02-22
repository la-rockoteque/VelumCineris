"""
Monster entity model for D&D 5e.

Provides type-safe validation for monster/creature data from Google Sheets.
"""

from pydantic import Field
from typing import Optional, List, Dict, Any, Union, Literal
import pandas as pd
import re
from fractions import Fraction

from ..base import BaseEntity
from ..fields.stats import Speed, AbilityScores

# Valid size codes
SizeType = Literal["T", "S", "M", "L", "H", "G"]

# Valid alignment codes
AlignmentType = Literal["L", "N", "C", "G", "E", "A", "U"]


class Monster(BaseEntity):
    """
    D&D 5e Monster/Creature model.

    Represents a creature in 5etools JSON format.
    """

    # Basic info
    size: List[SizeType] = Field(..., description="Size codes (T/S/M/L/H/G)")
    type: Union[str, Dict[str, Any]] = Field(..., description="Creature type (lowercase)")
    alignment: List[AlignmentType] = Field(..., description="Alignment codes")

    # Combat stats
    ac: List[Dict[str, Any]] = Field(..., description="Armor class with source")
    hp: Dict[str, Any] = Field(..., description="Hit points (average, formula)")
    speed: Dict[str, int] = Field(..., description="Movement speeds")

    # Ability scores (stored directly as int fields, not nested)
    str_: int = Field(..., alias="str", description="Strength score")
    dex: int = Field(..., description="Dexterity score")
    con: int = Field(..., description="Constitution score")
    int_: int = Field(..., alias="int", description="Intelligence score")
    wis: int = Field(..., description="Wisdom score")
    cha: int = Field(..., description="Charisma score")

    # Skills and saves
    skill: Optional[Dict[str, str]] = Field(None, description="Skill proficiencies")
    save: Optional[Dict[str, str]] = Field(None, description="Saving throw bonuses")
    passive: Optional[int] = Field(None, description="Passive Perception")

    # Resistances/immunities (can be mixed list of strings and dicts)
    immune: Optional[List[Union[str, Dict[str, Any]]]] = Field(
        None, description="Damage immunities"
    )
    resist: Optional[Union[List[str], List[Dict[str, Any]]]] = Field(
        None, description="Damage resistances"
    )
    vulnerable: Optional[List[str]] = Field(None, description="Damage vulnerabilities")
    conditionImmune: Optional[List[str]] = Field(None, description="Condition immunities")

    # Languages
    languages: Optional[List[str]] = Field(None, description="Known languages")

    # Challenge
    cr: str = Field(..., description="Challenge rating (as fraction string)")

    # Abilities
    trait: Optional[List[Dict[str, Any]]] = Field(None, description="Traits/features")
    action: Optional[List[Dict[str, Any]]] = Field(None, description="Actions")
    reaction: Optional[List[Dict[str, Any]]] = Field(None, description="Reactions")
    legendary: Optional[List[Dict[str, Any]]] = Field(None, description="Legendary actions")
    legendaryActions: Optional[int] = Field(None, description="Number of legendary actions")
    legendaryHeader: Optional[List[str]] = Field(None, description="Legendary actions header")

    # Visual
    tokenUrl: Optional[str] = Field(None, description="Token image URL")

    @staticmethod
    def parse_speed(value) -> Optional[int]:
        """Parse speed value from various formats."""
        if pd.isna(value):
            return None
        if isinstance(value, (int, float)):
            return int(value)
        if isinstance(value, str):
            match = re.search(r'(\d+)', value)
            return int(match.group(1)) if match else None
        return None

    @staticmethod
    def parse_entries(raw_text: str) -> List[Dict[str, Any]]:
        """Parse entries from text with ':: ' separator."""
        entries = []
        for text in raw_text.split("\n"):
            parts = text.split(":: ", 1)
            if len(parts) == 2:
                name, entry = parts
                entries.append({
                    "name": name.strip(),
                    "entries": [entry.strip()]
                })
            elif text.strip():
                # Single entry without name
                entries.append({
                    "name": "",
                    "entries": [text.strip()]
                })
        return entries

    @staticmethod
    def parse_skills(raw_text: str) -> Dict[str, str]:
        """Parse skills from text like 'Perception +4, Stealth +5'."""
        pattern = re.compile(
            r"(?:^|[,\n;]\s*)"
            r"([A-Z]{3}|[A-Za-z][A-Za-z'/-]*(?:\s+[A-Za-z'/-]+)*)"
            r"\s*([+-]\d+)",
            re.IGNORECASE
        )
        skills = {}
        for m in pattern.finditer(raw_text):
            name = m.group(1).strip().lower()
            skills[name] = m.group(2)
        return skills

    @staticmethod
    def parse_saves(raw_text: str) -> Dict[str, str]:
        """Parse saving throws from text like 'STR +13, DEX +7'."""
        pattern = re.compile(r"([A-Z][a-z]{2})\s*([+-]\d+)")
        saves = {}
        key_map = {
            "STR": "str", "Str": "str",
            "DEX": "dex", "Dex": "dex",
            "CON": "con", "Con": "con",
            "INT": "int", "Int": "int",
            "WIS": "wis", "Wis": "wis",
            "CHA": "cha", "Cha": "cha"
        }
        for stat, value in pattern.findall(raw_text):
            if stat in key_map:
                saves[key_map[stat]] = value
        return saves

    @staticmethod
    def parse_immunities(raw_text: str) -> Union[List[str], List[Dict[str, Any]]]:
        """Parse damage immunities with special conditions."""
        DMG = {
            "acid", "cold", "fire", "force", "lightning", "necrotic",
            "poison", "psychic", "radiant", "thunder"
        }
        BPS = {"bludgeoning", "piercing", "slashing"}

        immunities = []
        raw_lower = raw_text.lower()

        # Check for standard damage types
        for immunity in DMG:
            if immunity in raw_lower:
                immunities.append(immunity)

        # Check for conditional immunities (e.g., "from nonmagical weapons")
        if "from" in raw_lower:
            special_immunities = []
            fluff = raw_text.split(" from ")[1]
            for immunity in BPS:
                if immunity in raw_lower:
                    special_immunities.append(immunity)
            if special_immunities:
                immunities.append({
                    "immune": special_immunities,
                    "note": f"from {fluff.lower()}"
                })

        return immunities if immunities else []

    @classmethod
    def from_row(cls, row: pd.Series, source: str, json_source: str) -> 'Monster':
        """
        Create Monster from DataFrame row.

        Args:
            row: DataFrame row from Google Sheets
            source: Source filter (e.g., "ORIO")
            json_source: JSON source identifier (e.g., "GuideToOrimond")

        Returns:
            Validated Monster instance
        """
        name = row.get("Name", "Unnamed Creature")

        # Parse speed
        speed_dict = {}
        if (walk := cls.parse_speed(row.get("Speed (Walking)"))) is not None:
            speed_dict["walk"] = walk
        if (fly := cls.parse_speed(row.get("Speed (Flying)"))) is not None:
            speed_dict["fly"] = fly
        if (swim := cls.parse_speed(row.get("Speed (Swimming)"))) is not None:
            speed_dict["swim"] = swim
        if (burrow := cls.parse_speed(row.get("Speed (Burrowing)"))) is not None:
            speed_dict["burrow"] = burrow
        if (climb := cls.parse_speed(row.get("Speed (Climbing)"))) is not None:
            speed_dict["climb"] = climb

        # Helper to safely parse int with default
        def safe_int(value, default=10):
            if pd.isna(value):
                return default
            try:
                return int(value)
            except (ValueError, TypeError):
                return default

        # Parse AC
        ac_list = [{
            "ac": safe_int(row.get("Armor Class"), 10),
            "from": [
                row.get("Armor Type") if pd.notnull(row.get("Armor Type"))
                else "natural armor"
            ]
        }]

        # Parse HP
        hp_dict = {
            "average": safe_int(row.get("Hit Points"), 1),
            "formula": f"{row.get('Hit Dice', '1d8')} + {safe_int(row.get('CON Mod'), 0)}"
        }

        # Parse saves
        saves = None
        if pd.notnull(row.get("Saving Throws")):
            saves = cls.parse_saves(row.get("Saving Throws"))

        # Parse skills
        skills = None
        if pd.notnull(row.get("Skills")):
            skills = cls.parse_skills(row.get("Skills"))

        # Parse immunities
        immunities = None
        if pd.notnull(row.get("Damage Immunities")):
            immunities = cls.parse_immunities(row.get("Damage Immunities"))

        # Parse condition immunities
        condition_immunities = None
        if pd.notnull(row.get("Condition Immunities")):
            condition_immunities = [
                ci.strip().lower()
                for ci in row.get("Condition Immunities").split(",")
            ]

        # Parse abilities
        actions = None
        if pd.notnull(row.get("Actions")):
            actions = cls.parse_entries(row.get("Actions"))

        reactions = None
        if pd.notnull(row.get("Reactions")):
            reactions = cls.parse_entries(row.get("Reactions"))

        traits = None
        if pd.notnull(row.get("Traits")):
            traits = cls.parse_entries(row.get("Traits"))

        legendary_actions = None
        legendary_count = None
        legendary_header = None
        if pd.notnull(row.get("Legendary Actions")):
            legendary_actions = cls.parse_entries(row.get("Legendary Actions"))
            legendary_count = 3
            legendary_header = [
                f"The {name} can take 3 legendary actions, choosing from the options below. "
                f"Only one legendary action can be used at a time and only at the end of another "
                f"creature's turn. The {name} regains spent legendary actions at the start of its turn."
            ]

        # Parse languages
        languages = None
        if pd.notnull(row.get("Languages")):
            languages = [lang.strip().lower() for lang in row.get("Languages").split(",")]

        # Parse CR
        cr_value = row.get("CR (Challenge Rating)", "0")
        try:
            cr = str(Fraction(cr_value))
        except (ValueError, TypeError):
            cr = "0"

        # Parse fluff
        fluff_entries = []
        if pd.notnull(row.get("Description")):
            fluff_entries.append(row.get("Description"))

        fluff_images = []
        if pd.notnull(row.get("Image URL")):
            fluff_images.append({
                "type": "image",
                "href": {
                    "type": "external",
                    "url": row.get("Image URL")
                }
            })

        fluff = {
            "entries": fluff_entries,
            "images": fluff_images
        } if fluff_entries or fluff_images else None

        # Parse size safely
        size_val = row.get("Size", "M")
        if pd.isna(size_val):
            size_val = "M"
        size_str = str(size_val)[:1].upper()

        # Parse alignment safely
        align_val = row.get("Alignment", "N")
        if pd.isna(align_val):
            align_val = "N"
        align_str = str(align_val)[:1].upper()

        return cls(
            source=json_source,
            name=name,
            size=[size_str],
            type=str(row.get("Type", "humanoid")).lower() if pd.notnull(row.get("Type")) else "humanoid",
            alignment=[align_str],
            ac=ac_list,
            hp=hp_dict,
            speed=speed_dict,
            str_=safe_int(row.get("STR"), 10),
            dex=safe_int(row.get("DEX"), 10),
            con=safe_int(row.get("CON"), 10),
            int_=safe_int(row.get("INT"), 10),
            wis=safe_int(row.get("WIS"), 10),
            cha=safe_int(row.get("CHA"), 10),
            skill=skills,
            save=saves,
            passive=safe_int(row.get("Passive Perception"), 10) if pd.notnull(row.get("Passive Perception")) else None,
            immune=immunities,
            conditionImmune=condition_immunities,
            languages=languages,
            cr=cr,
            trait=traits,
            action=actions,
            reaction=reactions,
            legendary=legendary_actions,
            legendaryActions=legendary_count,
            legendaryHeader=legendary_header,
            tokenUrl=row.get("Tokens URL") if pd.notnull(row.get("Tokens URL")) else None,
            fluff=fluff,
            entries=[],  # Monsters don't have entries field in 5etools
        )
