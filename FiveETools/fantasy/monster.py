import pandas as pd
from FiveETools.fantasy.sources import json_source
from FiveETools.gsheets_client import fantasy_sheets
import re
from fractions import Fraction

df_monster = fantasy_sheets.get_sheet("736393386")
df_monster.head()

def parse_speed(value):
  """Parse speed value, handling strings like '30 ft.', integers, floats, or NaN."""
  if pd.isna(value):
    return None
  if isinstance(value, (int, float)):
    return int(value)
  if isinstance(value, str):
    # Extract number from "30 ft." format
    match = re.search(r'(\d+)', value)
    return int(match.group(1)) if match else None
  return None

def parse_entries(raw_text):
  pattern = re.compile(r"([A-Z][^.]+?)\.\s+(.*?)(?=(?:[A-Z][^.]+?\.)|$)", re.S)
  entries = []

  for text in raw_text.split("\n"):
    name, entry = (text.split(":: ") + ["", ""])[:2]
    entries.append({
      "name": name,
      "entries": [entry]
    })
  return entries

DMG = {
  "acid","cold","fire","force","lightning","necrotic",
  "poison","psychic","radiant","thunder"
}

BPS = {"bludgeoning","piercing","slashing"}

def parse_immunities(raw_text):
  immunities = []
  for immunity in DMG:
    if immunity in raw_text.lower():
      immunities.append(immunity)
      
  if "from" in raw_text.lower():
    special_immunities = []
    fluff = raw_text.split(" from ")[1]
    for immunity in BPS:
      if immunity in raw_text.lower():
        special_immunities.append(immunity)
    immunities.append({
      "immune": special_immunities,
      "note": f"from {fluff.lower()}"
    })

def parse_skills(raw_text):
  # Matches:
  #  - "STR +13"
  #  - "Sleight of Hand +7"
  #  - "Animal Handling -1"
  # Works across commas/newlines: "Perception +4, Stealth +5"
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

def parse_saves(raw_text):
  # Regex to match things like STR +13
  pattern = re.compile(r"([A-Z][a-z]{2})\s*([+-]\d+)")
  saves = {}

  # Map abbreviations to lowercase keys
  key_map = {
    "STR": "str",
    "DEX": "dex",
    "CON": "con",
    "INT": "int",
    "WIS": "wis",
    "CHA": "cha"
  }

  for stat, value in pattern.findall(raw_text):
    if stat in key_map:
      saves[key_map[stat.upper()]] = value

  return saves

def row_to_monster(row):
    name = row.get("Name")
    languages = (
        row.get("Languages").lower().split(", ")
        if pd.notnull(row.get("Languages"))
        else []
    )
    return {
        "source": json_source,
        "name": name,
        "size": [row.get("Size")[:1].upper()],
        "type": row.get("Type").lower(),
        "alignment": [row.get("Alignment")[:1].upper()],
        "ac": [
            {
                "ac": row.get("Armor Class"),
                "from": [
                    row.get("Armor Type")
                    if pd.notnull(row.get("Armor Type"))
                    else "natural armor"
                ],
            }
        ],
        "hp": {
            "average": row.get("Hit Points"),
            "formula": f"{row.get('Hit Dice').lower()} + {row.get('CON Mod')}",
        },
        **(
            {"save": parse_saves(row.get("Saving Throws")),}
            if pd.notnull(row.get("save"))
            else {}
        ),
        "passive": row.get("Passive Perception"),
        "speed": {
            **(
                {"walk": walk_speed}
                if (walk_speed := parse_speed(row.get("Speed (Walking)"))) is not None
                else {}
            ),
            **(
                {"fly": fly_speed}
                if (fly_speed := parse_speed(row.get("Speed (Flying)"))) is not None
                else {}
            ),
            **(
                {"swim": swim_speed}
                if (swim_speed := parse_speed(row.get("Speed (Swimming)"))) is not None
                else {}
            ),
            **(
                {"burrow": burrow_speed}
                if (burrow_speed := parse_speed(row.get("Speed (Burrowing)"))) is not None
                else {}
            ),
        },
        "str": int(row.get("STR")),
        "dex": int(row.get("DEX")),
        "con": int(row.get("CON")),
        "int": int(row.get("INT")),
        "wis": int(row.get("WIS")),
        "cha": int(row.get("CHA")),
        **(
            {"action": parse_entries(row.get("Actions"))}
            if pd.notnull(row.get("Actions"))
            else {}
        ),
        **(
            {"reaction": parse_entries(row.get("Reactions"))}
            if pd.notnull(row.get("Reactions"))
            else {}
        ),
        **(
            {
                "legendaryActions": 3,
                "legendaryHeader": [
                    f"The {name} can take 3 legendary actions, choosing from the options below. Only one legendary action can be used at a time and only at the end of another creature's turn. The {name} regains spent legendary actions at the start of its turn."
                ],
                "legendary": parse_entries(row.get("Legendary Actions")),
            }
            if pd.notnull(row.get("Legendary Actions"))
            else {}
        ),
        **(
            {"trait": parse_entries(row.get("Traits"))}
            if pd.notnull(row.get("Traits"))
            else {}
        ),
        **(
            {"skill": parse_skills(row.get("Skills"))}
            if pd.notnull(row.get("Skills"))
            else {}
        ),
        **(
            {"immune": parse_immunities(row.get("Damage Immunities"))}
            if pd.notnull(row.get("Damage Immunities"))
            else {}
        ),
        **(
            {"conditionImmune": row.get("Condition Immunities").lower().split(", ")}
            if pd.notnull(row.get("Condition Immunities"))
            else {}
        ),
        # **({"languages":
        #       (languages[0] if len(languages) == 1 else languages[0])
        # } if pd.notnull(row.get("Languages")) else {}),
        "cr": f"{Fraction(row.get('CR (Challenge Rating)'))}",
        "tokenUrl": row.get("Tokens URL"),
        "fluff": {
            "entries": [row.get("Description")],
            "images": [
                {
                    "type": "image",
                    "href": {
                        "type": "external",
                        "url": row.get("Image URL"),
                    },
                }
            ],
        },
    }


monster_list = [
    row_to_monster(row)
    for index, row in df_monster.iterrows()
    if pd.notnull(row.get("Name"))
]

# NEW: Pydantic-based conversion for type safety
from Spreadsheet.converters.monster import MonsterConverter
from models.entities.monster import Monster
from typing import List

converter = MonsterConverter(fantasy_sheets)
monster_pydantic: List[Monster] = converter.convert_all(
    source_filter=None,  # Monsters don't use source filter by default
    source="ORIO",
    json_source=json_source
)
