"""
Monster entity model for D&D 5e.

Provides type-safe validation for monster/creature data from Google Sheets.
"""

from pydantic import Field
from typing import Optional, List, Dict, Any, Union, Literal
import re
from fractions import Fraction

from ..base import BaseEntity
from ..fields.stats import Speed, AbilityScores
from ..row_access import is_missing, optional_int, optional_text, row_value, split_csv

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
        if is_missing(value):
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
    def from_row(cls, row, source: str, json_source: str) -> 'Monster':
        """
        Create Monster from DataFrame row.

        Args:
            row: DataFrame row from Google Sheets
            source: Source filter (e.g., "ORIO")
            json_source: JSON source identifier (e.g., "GuideToOrimond")

        Returns:
            Validated Monster instance
        """
        name = optional_text(row_value(row, "Name")) or "Unnamed Creature"

        # Parse speed
        speed_dict = {}
        if (walk := cls.parse_speed(row_value(row, "Speed (Walking)"))) is not None:
            speed_dict["walk"] = walk
        if (fly := cls.parse_speed(row_value(row, "Speed (Flying)"))) is not None:
            speed_dict["fly"] = fly
        if (swim := cls.parse_speed(row_value(row, "Speed (Swimming)"))) is not None:
            speed_dict["swim"] = swim
        if (burrow := cls.parse_speed(row_value(row, "Speed (Burrowing)"))) is not None:
            speed_dict["burrow"] = burrow
        if (climb := cls.parse_speed(row_value(row, "Speed (Climbing)"))) is not None:
            speed_dict["climb"] = climb

        # Helper to safely parse int with default
        def safe_int(value, default=10):
            return optional_int(value, default)

        # Parse AC
        ac_list = [{
            "ac": safe_int(row_value(row, "Armor Class"), 10),
            "from": [
                optional_text(row_value(row, "Armor Type")) or "natural armor"
            ]
        }]

        # Parse HP
        hp_dict = {
            "average": safe_int(row_value(row, "Hit Points"), 1),
            "formula": f"{row_value(row, 'Hit Dice', '1d8')} + {safe_int(row_value(row, 'CON Mod'), 0)}"
        }

        # Parse saves
        saves = None
        saving_throws = optional_text(row_value(row, "Saving Throws"))
        if saving_throws:
            saves = cls.parse_saves(saving_throws)

        # Parse skills
        skills = None
        skills_text = optional_text(row_value(row, "Skills"))
        if skills_text:
            skills = cls.parse_skills(skills_text)

        # Parse immunities
        immunities = None
        damage_immunities = optional_text(row_value(row, "Damage Immunities"))
        if damage_immunities:
            immunities = cls.parse_immunities(damage_immunities)

        # Parse condition immunities
        condition_immunities = None
        condition_immunity_values = split_csv(row_value(row, "Condition Immunities"))
        if condition_immunity_values:
            condition_immunities = [ci.lower() for ci in condition_immunity_values]

        # Parse abilities
        actions = None
        actions_text = optional_text(row_value(row, "Actions"))
        if actions_text:
            actions = cls.parse_entries(actions_text)

        reactions = None
        reactions_text = optional_text(row_value(row, "Reactions"))
        if reactions_text:
            reactions = cls.parse_entries(reactions_text)

        traits = None
        traits_text = optional_text(row_value(row, "Traits"))
        if traits_text:
            traits = cls.parse_entries(traits_text)

        legendary_actions = None
        legendary_count = None
        legendary_header = None
        legendary_text = optional_text(row_value(row, "Legendary Actions"))
        if legendary_text:
            legendary_actions = cls.parse_entries(legendary_text)
            legendary_count = 3
            legendary_header = [
                f"The {name} can take 3 legendary actions, choosing from the options below. "
                f"Only one legendary action can be used at a time and only at the end of another "
                f"creature's turn. The {name} regains spent legendary actions at the start of its turn."
            ]

        # Parse languages
        languages = None
        language_values = split_csv(row_value(row, "Languages"))
        if language_values:
            languages = [lang.lower() for lang in language_values]

        # Parse CR
        cr_value = row_value(row, "CR (Challenge Rating)", "0")
        try:
            cr = str(Fraction(cr_value))
        except (ValueError, TypeError):
            cr = "0"

        # Parse fluff
        fluff_entries = []
        description = optional_text(row_value(row, "Description"))
        if description:
            fluff_entries.append(description)

        fluff_images = []
        image_url = optional_text(row_value(row, "Image URL"))
        if image_url:
            fluff_images.append({
                "type": "image",
                "href": {
                    "type": "external",
                    "url": image_url
                }
            })

        fluff = {
            "entries": fluff_entries,
            "images": fluff_images
        } if fluff_entries or fluff_images else None

        # Parse size safely
        size_val = row_value(row, "Size", "M")
        if is_missing(size_val):
            size_val = "M"
        size_str = str(size_val)[:1].upper()

        # Parse alignment safely
        align_val = row_value(row, "Alignment", "N")
        if is_missing(align_val):
            align_val = "N"
        align_str = str(align_val)[:1].upper()

        return cls(
            source=json_source,
            name=name,
            size=[size_str],
            type=(optional_text(row_value(row, "Type")) or "humanoid").lower(),
            alignment=[align_str],
            ac=ac_list,
            hp=hp_dict,
            speed=speed_dict,
            str_=safe_int(row_value(row, "STR"), 10),
            dex=safe_int(row_value(row, "DEX"), 10),
            con=safe_int(row_value(row, "CON"), 10),
            int_=safe_int(row_value(row, "INT"), 10),
            wis=safe_int(row_value(row, "WIS"), 10),
            cha=safe_int(row_value(row, "CHA"), 10),
            skill=skills,
            save=saves,
            passive=None if is_missing(row_value(row, "Passive Perception")) else safe_int(row_value(row, "Passive Perception"), 10),
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
            tokenUrl=optional_text(row_value(row, "Tokens URL")),
            fluff=fluff,
            entries=[],  # Monsters don't have entries field in 5etools
        )
