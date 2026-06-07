"""Rebalance and audit the Orimond spell compendium CSV."""

from __future__ import annotations

import argparse
import csv
import re
from collections import Counter
from pathlib import Path
from typing import Iterable


AUDIT_COLUMNS = [
    "Audit - Resolution Model",
    "Audit - Cantrip Decision",
    "Audit - Damage Budget",
    "Audit - Rider Budget",
    "Audit - Damage Verdict",
    "Audit - Permanent Effect Verdict",
    "Audit - Original Class Verdict",
    "Audit - Suggested Class Additions",
    "Audit - Suggested Class Removals",
    "Audit - Class Rationale",
    "Audit - Action Economy Verdict",
    "Audit - Upcasting Verdict",
    "Audit - Overall Balance Verdict",
    "Audit - Recommended Change Summary",
]

ABILITIES = (
    "Strength",
    "Dexterity",
    "Constitution",
    "Intelligence",
    "Wisdom",
    "Charisma",
)
CONDITIONS = (
    "Blinded",
    "Charmed",
    "Deafened",
    "Frightened",
    "Grappled",
    "Incapacitated",
    "Invisible",
    "Paralyzed",
    "Petrified",
    "Poisoned",
    "Prone",
    "Restrained",
    "Stunned",
    "Unconscious",
    "Exhaustion",
)
DAMAGE_TYPES = (
    "Acid",
    "Bludgeoning",
    "Cold",
    "Fire",
    "Force",
    "Lightning",
    "Necrotic",
    "Piercing",
    "Poison",
    "Psychic",
    "Radiant",
    "Slashing",
    "Thunder",
)
STRONG_RIDERS = {
    "charmed",
    "frightened",
    "incapacitated",
    "invisible",
    "paralyzed",
    "petrified",
    "restrained",
    "stunned",
    "unconscious",
}
OUTLIERS = {
    "Eyes Behind the Kiss",
    "Festering Graze",
    "Prism Shear",
    "Formula of Unraveling",
    "Fragmentation Rift",
    "Strike from the Loom",
}
PERMANENT_MARKERS = (
    "permanent",
    "until dispelled",
    "until cured",
    "until revoked",
    "until nullified",
    "until fulfilled",
    "until broken",
)
TECHNO_WORDS = (
    "algorithm",
    "biometric",
    "circuit",
    "computation",
    "data",
    "device",
    "digital",
    "electromagnetic",
    "industrial",
    "machine",
    "network",
    "protocol",
    "record",
    "sensor",
    "signal",
    "system",
)
RITUAL_WORDS = (
    "communicat",
    "detect",
    "identify",
    "ledger",
    "legal",
    "locate",
    "map",
    "record",
    "ritual",
    "translate",
    "truth",
    "ward",
)
CLASS_WORDS = {
    "Artificer": (
        "alchemy",
        "circuit",
        "construct",
        "device",
        "formula",
        "industrial",
        "machine",
        "object",
        "protocol",
        "repair",
        "system",
        "tool",
        "ward",
    ),
    "Bard": (
        "attention",
        "charm",
        "emotion",
        "fear",
        "glamour",
        "language",
        "memory",
        "music",
        "performance",
        "reputation",
        "song",
        "speech",
        "story",
    ),
    "Cleric": (
        "consecrat",
        "divine",
        "exorcis",
        "heal",
        "judgment",
        "restoration",
        "rite",
        "sacred",
        "soul",
    ),
    "Druid": (
        "animal",
        "beast",
        "decay",
        "disease",
        "forest",
        "nature",
        "plant",
        "rot",
        "spore",
        "terrain",
        "weather",
        "wild",
    ),
    "Ranger": (
        "ambush",
        "mark",
        "mobility",
        "pursu",
        "stealth",
        "survival",
        "terrain",
        "track",
        "trap",
    ),
    "Paladin": (
        "aura",
        "courage",
        "divine command",
        "judgment",
        "martial",
        "oath",
        "protect",
        "punish",
        "smite",
        "valor",
    ),
    "Sorcerer": (
        "anomal",
        "blood",
        "body",
        "innate",
        "mutation",
        "raw energy",
        "self",
        "unstable",
    ),
    "Warlock": (
        "bargain",
        "curse",
        "debt",
        "forbidden",
        "name",
        "occult",
        "pact",
        "patron",
        "summon",
    ),
    "Wizard": (
        "analyt",
        "codified",
        "formula",
        "ledger",
        "planar",
        "record",
        "ritual",
        "spatial",
        "study",
    ),
}

CLASS_LEVEL_TARGETS = {
    "Artificer": (8, 14, 13, 10, 8, 7, 0, 0, 0, 0),
    "Bard": (10, 19, 20, 14, 7, 14, 6, 9, 4, 4),
    "Cleric": (8, 17, 17, 18, 11, 12, 6, 5, 3, 3),
    "Druid": (6, 12, 19, 14, 13, 13, 6, 4, 5, 3),
    "Paladin": (0, 14, 9, 10, 8, 9, 0, 0, 0, 0),
    "Ranger": (0, 13, 12, 11, 5, 4, 0, 0, 0, 0),
    "Sorcerer": (16, 22, 26, 23, 11, 12, 11, 8, 6, 5),
    "Warlock": (12, 15, 16, 16, 6, 5, 11, 5, 7, 7),
    "Wizard": (10, 18, 21, 17, 14, 14, 12, 9, 8, 7),
}
CLASS_SCHOOL_AFFINITY = {
    "Artificer": {"Abjuration": 3, "Divination": 2, "Transmutation": 3},
    "Bard": {"Divination": 2, "Enchantment": 4, "Illusion": 4},
    "Cleric": {"Abjuration": 3, "Divination": 2, "Evocation": 2, "Necromancy": 3},
    "Druid": {"Conjuration": 2, "Divination": 2, "Necromancy": 2, "Transmutation": 4},
    "Paladin": {"Abjuration": 4, "Enchantment": 1, "Evocation": 3},
    "Ranger": {"Conjuration": 2, "Divination": 4, "Transmutation": 3},
    "Sorcerer": {"Conjuration": 1, "Evocation": 4, "Transmutation": 3},
    "Warlock": {"Conjuration": 3, "Enchantment": 3, "Illusion": 2, "Necromancy": 4},
    "Wizard": {
        "Abjuration": 2,
        "Conjuration": 2,
        "Divination": 2,
        "Enchantment": 2,
        "Evocation": 2,
        "Illusion": 2,
        "Necromancy": 2,
        "Transmutation": 2,
    },
}

LEVEL_RE = re.compile(r"(\d)")
DICE_RE = re.compile(r"\b(\d+)d(\d+)(?:\s*([+-])\s*(\d+))?\b", re.IGNORECASE)
SAVE_RE = re.compile(
    rf"\b({'|'.join(ABILITIES)})\b(?:\s+\([^)]+\))?\s+saving throw",
    re.IGNORECASE,
)
CONDITION_RE = re.compile(rf"\b({'|'.join(CONDITIONS)})\b", re.IGNORECASE)
DAMAGE_TYPE_RE = re.compile(rf"\b({'|'.join(DAMAGE_TYPES)})\s+damage\b", re.IGNORECASE)


def unique(values: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        normalized = value.strip().lower()
        if normalized and normalized not in seen:
            seen.add(normalized)
            result.append(value.strip())
    return result


def level_number(value: str) -> int:
    match = LEVEL_RE.search(value)
    return int(match.group(1)) if match else 0


def normalize_level(value: str) -> str:
    level = level_number(value)
    if level == 0:
        return "0-Cantrip"
    suffix = {1: "st", 2: "nd", 3: "rd"}.get(level, "th")
    return f"{level}{suffix}-level"


def normalize_boolean(value: str) -> str:
    return "TRUE" if value.strip().lower() in {"true", "1", "yes", "y"} else "FALSE"


def normalize_casting_time(value: str) -> str:
    cleaned = value.strip()
    replacements = {
        "1 minutes": "1 minute",
        "1 hours": "1 hour",
    }
    return replacements.get(cleaned, cleaned)


def normalize_duration(value: str) -> str:
    cleaned = value.strip()
    cleaned = re.sub(r"(?i)^instant$", "Instantaneous", cleaned)
    cleaned = re.sub(r"(?i)^instantaneous$", "Instantaneous", cleaned)
    cleaned = re.sub(r"(?i)^premanent$", "Permanent", cleaned)
    cleaned = re.sub(r"(?i)^permanent$", "Permanent", cleaned)
    cleaned = re.sub(r"(?i)\b1 minutes\b", "1 minute", cleaned)
    cleaned = re.sub(r"(?i)\b1 rounds\b", "1 round", cleaned)
    cleaned = re.sub(r"(?i)\b1 hours?\b", "1 hour", cleaned)
    cleaned = re.sub(r"(?i)^up to\b", "Up to", cleaned)
    return cleaned


def normalize_components(value: str) -> str:
    order = ["Verbal", "Somatic", "Material"]
    present = {part.strip().lower() for part in value.split(",")}
    return ", ".join(part for part in order if part.lower() in present)


def text_for(row: dict[str, str]) -> str:
    return " ".join(
        row.get(field, "")
        for field in ("Spell Name", "Description", "Notes", "Clarification", "Flavor")
    ).lower()


def contains_keyword(text: str, keyword: str) -> bool:
    return bool(re.search(rf"\b{re.escape(keyword)}", text))


def extract_label(text: str, label: str) -> str:
    pattern = re.compile(
        rf"(?is)(?:[•*-]\s*)?{label}\s*:\s*(.+?)(?=\n\s*(?:[•*-]\s*)?"
        r"(?:failure|fail|success)\s*:|\n\s*\n|$)"
    )
    match = pattern.search(text)
    return re.sub(r"\s+", " ", match.group(1)).strip() if match else ""


def infer_damage_type(row: dict[str, str]) -> str:
    text = row["Description"]
    found = unique(match.title() for match in DAMAGE_TYPE_RE.findall(text))
    if found:
        return ", ".join(found)
    hints = {
        "burn": "Fire",
        "flame": "Fire",
        "frost": "Cold",
        "ice": "Cold",
        "lightning": "Lightning",
        "thunder": "Thunder",
        "poison": "Poison",
        "psychic": "Psychic",
        "mind": "Psychic",
        "radiant": "Radiant",
        "necrot": "Necrotic",
        "decay": "Necrotic",
        "force": "Force",
        "slash": "Slashing",
        "pierc": "Piercing",
        "crush": "Bludgeoning",
    }
    lowered = text_for(row)
    for word, damage_type in hints.items():
        if word in lowered:
            return damage_type
    return {
        "Necromancy": "Necrotic",
        "Evocation": "Force",
        "Illusion": "Psychic",
    }.get(row["School"], "Force")


def infer_damage_formula(text: str) -> str:
    matches = unique(match.group(0) for match in DICE_RE.finditer(text))
    return ", ".join(matches[:3])


def average_damage(formula: str) -> float | None:
    match = DICE_RE.search(formula)
    if not match:
        return None
    count, die = int(match.group(1)), int(match.group(2))
    modifier = int(match.group(4) or 0)
    if match.group(3) == "-":
        modifier *= -1
    return count * (die + 1) / 2 + modifier


def class_list(value: str) -> list[str]:
    return unique(part.strip() for part in value.split(",") if part.strip())


def class_score(row: dict[str, str], class_name: str) -> int:
    text = text_for(row)
    return sum(contains_keyword(text, word) for word in CLASS_WORDS[class_name])


def class_affinity(
    row: dict[str, str],
    class_name: str,
    original_classes: set[str],
) -> int:
    text = text_for(row)
    score = class_score(row, class_name) * 8
    score += CLASS_SCHOOL_AFFINITY[class_name].get(row["School"], 0)
    score += 16 if class_name in original_classes else 0
    score += (
        2
        if row["Ritual"] == "TRUE" and class_name in {"Artificer", "Cleric", "Wizard"}
        else 0
    )
    score += 2 if row["Techno Magic"] == "TRUE" and class_name == "Artificer" else 0
    score += 2 if row["Blood Pact"] == "TRUE" and class_name == "Warlock" else 0
    score += 2 if row["Damage"].strip() and class_name in {"Paladin", "Sorcerer"} else 0
    score += (
        2
        if row["Condition"].strip() and class_name in {"Bard", "Cleric", "Warlock"}
        else 0
    )
    score += (
        2 if row["Range"].strip().lower() == "self" and class_name == "Sorcerer" else 0
    )
    score += (
        1
        if any(word in text for word in ("weapon", "strike", "attack"))
        and class_name in {"Paladin", "Ranger"}
        else 0
    )
    return score


def normalize_row(row: dict[str, str]) -> None:
    row["Level"] = normalize_level(row["Level"])
    row["Casting Time"] = normalize_casting_time(row["Casting Time"])
    row["Duration"] = normalize_duration(row["Duration"])
    row["Components"] = normalize_components(row["Components"])
    for field in ("Ritual", "Techno Magic", "Concentration"):
        row[field] = normalize_boolean(row[field])
    if row["Blood Pact"].strip() and row["Blood Pact"].strip().lower() not in {
        "true",
        "false",
    }:
        existing = row["Blood Pact Effect"].strip()
        row["Blood Pact Effect"] = "; ".join(
            part for part in (existing, row["Blood Pact"].strip()) if part
        )
        row["Blood Pact"] = "TRUE"
    else:
        row["Blood Pact"] = normalize_boolean(row["Blood Pact"])


def fill_metadata(row: dict[str, str]) -> None:
    description = row["Description"]
    saves = unique(match.title() for match in SAVE_RE.findall(description))
    if saves and not row["Saving Throw"].strip():
        row["Saving Throw"] = ", ".join(saves)

    conditions = unique(match.title() for match in CONDITION_RE.findall(description))
    if conditions and not row["Condition"].strip():
        row["Condition"] = ", ".join(conditions)

    if not row["Damage"].strip() and re.search(r"(?i)\bdamage\b", description):
        row["Damage"] = infer_damage_formula(description)
    explicit_damage_types = unique(
        match.title() for match in DAMAGE_TYPE_RE.findall(description)
    )
    if row["Damage"].strip() and explicit_damage_types:
        row["Damage Type"] = ", ".join(explicit_damage_types)
    elif row["Damage"].strip() and not row["Damage Type"].strip():
        row["Damage Type"] = infer_damage_type(row)
    elif row["Damage Type"].strip():
        row["Damage Type"] = ", ".join(
            part.strip().title() for part in row["Damage Type"].split(",")
        )

    if row["Saving Throw"].strip():
        if not row["Success"].strip():
            row["Success"] = extract_label(description, "success(?:ful save)?")
        if not row["Fail"].strip():
            row["Fail"] = extract_label(description, "fail(?:ure|ed save)?")
        if not row["Success"].strip():
            row["Success"] = (
                "The target takes half damage and suffers no additional effect."
                if row["Damage"].strip()
                else "The target is unaffected."
            )
        if not row["Fail"].strip():
            effects = []
            if row["Damage"].strip():
                effects.append("takes the spell's full damage")
            if row["Condition"].strip():
                effects.append(f"is {row['Condition'].split(',')[0].strip().lower()}")
            row["Fail"] = (
                "The target " + " and ".join(effects) + "."
                if effects
                else "The target suffers the spell's described effect."
            )
        ongoing_condition = row["Condition"].strip() and row["Duration"] not in {
            "",
            "Instantaneous",
            "1 turn",
            "1 round",
        }
        resolution_text = f"{description} {row['Fail']}".lower()
        if (
            ongoing_condition
            and not any(
                marker in row["Duration"].lower() for marker in PERMANENT_MARKERS
            )
            and "repeat" not in resolution_text
            and not any(
                word in resolution_text for word in ("ends early", "breaks the effect")
            )
        ):
            row["Fail"] = (
                f"{row['Fail'].rstrip()} The target repeats the saving throw at the end "
                "of each of its turns, ending the effect on a success."
            )


def resolution_model(row: dict[str, str]) -> str:
    text = text_for(row)
    if row["Saving Throw"].strip():
        return "Saving Throw"
    if "spell attack" in text:
        return "Spell Attack"
    if (
        "contested" in text
        or row["Skill Check"].strip()
        or row["Ability Check"].strip()
    ):
        return "Contested Check"
    if any(
        word in text
        for word in ("willing", "incapacitated", "restrained", "prerequisite")
    ):
        return "Automatic with prerequisite"
    if any(word in text for word in ("avoid", "crosses", "enters the area", "hazard")):
        return "Environmental with avoidance rules"
    return "Automatic with prerequisite"


def cantrip_score(row: dict[str, str]) -> int:
    text = text_for(row)
    score = 0
    score += 4 * sum(condition in text for condition in STRONG_RIDERS)
    score += 3 * sum(
        phrase in text
        for phrase in (
            "cannot take reactions",
            "advantage",
            "disadvantage",
            "battlefield",
            "obscured",
            "spell attack and hits",
        )
    )
    score += 2 * sum(
        phrase in text
        for phrase in (
            "for 1 minute",
            "up to 1 minute",
            "concentration",
            "until the spell ends",
        )
    )
    score += 2 if row["Casting Time"] in {"Reaction", "Bonus Action"} else 0
    return score


def classify_damage(row: dict[str, str]) -> None:
    value = average_damage(row["Damage"])
    if value is None:
        row["Audit - Damage Budget"] = "No explicit damage formula"
        row["Audit - Rider Budget"] = (
            "Strong rider"
            if any(c in text_for(row) for c in STRONG_RIDERS)
            else "No strong rider"
        )
        row["Audit - Damage Verdict"] = (
            "Needs Manual Review" if "damage" in text_for(row) else "Acceptable"
        )
        return

    level = level_number(row["Level"])
    ranges = {
        0: (3.5, 5.5),
        1: (9, 13.5),
        2: (13.5, 18),
        3: (22.5, 27),
        4: (27, 36),
        5: (36, 45),
        6: (45, 54),
        7: (60.5, 71.5),
        8: (66, 77),
        9: (77, 110),
    }
    low, high = ranges[level]
    text = text_for(row)
    area = bool(row["Area"].strip()) or any(
        word in text
        for word in ("cone", "radius", "sphere", "each creature", "all creatures")
    )
    strong_rider = any(condition in text for condition in STRONG_RIDERS) or any(
        phrase in text
        for phrase in (
            "cannot take reactions",
            "vulnerability",
            "permanent",
            "starts its turn",
        )
    )
    if area:
        low, high = low * 0.65, high * 0.8
    if strong_rider:
        low, high = low * 0.5, high * 0.75
    row["Audit - Damage Budget"] = f"{low:.1f}-{high:.1f} expected; {value:.1f} listed"
    row["Audit - Rider Budget"] = (
        "Strong rider: reduced damage budget" if strong_rider else "No strong rider"
    )
    if row["Spell Name"].strip() in OUTLIERS:
        verdict = "Needs Manual Review"
    elif value < low * 0.8:
        verdict = "Too Low"
    elif value > high * 1.2:
        verdict = "Too High Because of Rider" if strong_rider else "Too High"
    else:
        verdict = "Acceptable"
    row["Audit - Damage Verdict"] = verdict


def audit_permanent(row: dict[str, str]) -> None:
    text = text_for(row)
    if not any(
        marker in row["Duration"].lower() or marker in text
        for marker in PERMANENT_MARKERS
    ):
        row["Audit - Permanent Effect Verdict"] = "Safe"
        return
    constraints = sum(
        bool(value.strip())
        for value in (
            row["Cost"],
            row["Arcane Strain"],
            row["Component Description (Material)"],
        )
    )
    constraints += row["Blood Pact"] == "TRUE"
    constraints += sum(
        phrase in text
        for phrase in (
            "willing",
            "incapacitated",
            "restrained",
            "repeat the saving throw",
            "until dispelled",
            "can be removed",
            "restoration",
            "once",
            "immune",
        )
    )
    if constraints >= 3:
        verdict = "Safe"
    elif not row["Saving Throw"].strip() and any(
        word in text for word in ("target", "creature")
    ):
        verdict = "Needs Save"
    elif not any(
        phrase in text
        for phrase in ("dispel", "removed", "restoration", "cured", "broken")
    ):
        verdict = "Needs Dispel Method"
    elif not row["Cost"].strip() and not row["Blood Pact"].strip():
        verdict = "Needs Cost"
    else:
        verdict = "Needs Manual Review"
    row["Audit - Permanent Effect Verdict"] = verdict


def set_concentration(row: dict[str, str]) -> None:
    text = text_for(row)
    persistent = row["Duration"] not in {"", "Instantaneous", "1 turn", "1 round"}
    hostile_control = bool(row["Condition"].strip()) or any(
        phrase in text
        for phrase in (
            "cannot take reactions",
            "controls movement",
            "difficult terrain",
            "starts its turn",
            "summon",
        )
    )
    if (
        persistent
        and hostile_control
        and not any(marker in row["Duration"].lower() for marker in PERMANENT_MARKERS)
    ):
        row["Concentration"] = "TRUE"


def assign_rituals(rows: list[dict[str, str]], target: int = 45) -> None:
    candidates = []
    for row in rows:
        text = text_for(row)
        score = sum(contains_keyword(text, word) for word in RITUAL_WORDS)
        score += row["Casting Time"] in {"1 minute", "10 minutes", "1 hour"}
        score += row["Damage"].strip() == "" and row["Condition"].strip() == ""
        if score:
            candidates.append((score, row["Spell Name"], row))
    current = sum(row["Ritual"] == "TRUE" for row in rows)
    for _, _, row in sorted(candidates, key=lambda item: (-item[0], item[1])):
        if current >= target:
            break
        if row["Ritual"] == "FALSE":
            row["Ritual"] = "TRUE"
            current += 1


def rebalance_cantrips(rows: list[dict[str, str]], promote_count: int = 30) -> None:
    cantrips = [row for row in rows if level_number(row["Level"]) == 0]
    ranked = sorted(cantrips, key=lambda row: (-cantrip_score(row), row["Spell Name"]))
    promoted = {row["Spell Name"] for row in ranked[:promote_count]}
    for row in cantrips:
        if row["Spell Name"] in promoted:
            row["Level"] = "1st-level"
            row["Audit - Cantrip Decision"] = "Promote to 1st-level"
        elif row["Ritual"] == "TRUE" and row["Damage"].strip() == "":
            row["Audit - Cantrip Decision"] = "Convert to Ritual"
        else:
            row["Audit - Cantrip Decision"] = "Keep as Cantrip"
    for row in rows:
        if not row["Audit - Cantrip Decision"]:
            row["Audit - Cantrip Decision"] = "Needs Manual Review"


def rebalance_schools(rows: list[dict[str, str]]) -> None:
    illusion_count = sum(row["School"] == "Illusion" for row in rows)
    candidates = []
    for row in rows:
        text = text_for(row)
        score = sum(
            word in text
            for word in (
                "conceal",
                "decoy",
                "false presence",
                "illusion",
                "perception",
                "unseen",
            )
        )
        if row["School"] == "Transmutation" and score:
            candidates.append((score, row["Spell Name"], row))
    for _, _, row in sorted(candidates, key=lambda item: (-item[0], item[1])):
        if illusion_count >= 38:
            break
        row["School"] = "Illusion"
        row["School ABRV"] = "I"
        illusion_count += 1


def rebalance_classes(rows: list[dict[str, str]]) -> None:
    additions: dict[str, list[str]] = {row["Spell Name"]: [] for row in rows}
    removals: dict[str, list[str]] = {row["Spell Name"]: [] for row in rows}
    original = {id(row): set(class_list(row["Class"])) for row in rows}
    assigned: dict[int, list[str]] = {id(row): [] for row in rows}

    for level in range(10):
        level_rows = [row for row in rows if level_number(row["Level"]) == level]
        remaining = {
            class_name: targets[level]
            for class_name, targets in CLASS_LEVEL_TARGETS.items()
            if targets[level] > 0
        }
        primary_order = sorted(
            level_rows,
            key=lambda row: (
                -max(
                    class_affinity(row, class_name, original[id(row)])
                    for class_name in remaining
                ),
                row["Spell Name"].strip(),
            ),
        )
        for row in primary_order:
            available = [
                class_name for class_name, count in remaining.items() if count > 0
            ]
            class_name = max(
                available,
                key=lambda candidate: (
                    class_affinity(row, candidate, original[id(row)]),
                    remaining[candidate] / CLASS_LEVEL_TARGETS[candidate][level],
                ),
            )
            assigned[id(row)].append(class_name)
            remaining[class_name] -= 1

        for class_name, count in remaining.items():
            candidates = sorted(
                (row for row in level_rows if class_name not in assigned[id(row)]),
                key=lambda row: (
                    -class_affinity(row, class_name, original[id(row)]),
                    row["Spell Name"].strip(),
                ),
            )
            for row in candidates[:count]:
                assigned[id(row)].append(class_name)

    for row in rows:
        revised = assigned[id(row)]
        original_standard = original[id(row)] & set(CLASS_LEVEL_TARGETS)
        revised_set = set(revised)
        additions[row["Spell Name"]] = sorted(revised_set - original_standard)
        removals[row["Spell Name"]] = sorted(original_standard - revised_set)
        row["Class"] = ", ".join(revised)

    for row in rows:
        added = additions[row["Spell Name"]]
        removed = removals[row["Spell Name"]]
        row["Audit - Suggested Class Additions"] = ", ".join(added)
        row["Audit - Suggested Class Removals"] = ", ".join(removed)
        if added and removed:
            verdict = "Narrow Access"
        elif added:
            verdict = "Broaden Access"
        elif removed:
            verdict = "Remove Classes"
        else:
            verdict = "Keep"
        row["Audit - Original Class Verdict"] = verdict
        rationale = []
        if added:
            rationale.append(f"Added thematic access for {', '.join(added)}")
        if removed:
            rationale.append(
                f"Removed non-thematic/high-level access for {', '.join(removed)}"
            )
        row["Audit - Class Rationale"] = (
            "; ".join(rationale) or "Existing access is thematic."
        )


def rebalance_action_economy(rows: list[dict[str, str]]) -> None:
    reaction_candidates = []
    bonus_candidates = []
    for row in rows:
        if (
            row["Casting Time"] == "Reaction"
            and not row["Trigger"].strip()
            and not contains_keyword(text_for(row), "when")
        ):
            row["Casting Time"] = "Action"
            row["Casting Type"] = "Action"
            row["Audit - Action Economy Verdict"] = "Keep Action"
        if row["Casting Time"] != "Action":
            continue
        text = text_for(row)
        reaction_score = sum(
            phrase in text
            for phrase in (
                "when a creature",
                "when you",
                "when an attack",
                "when targeted",
                "crosses",
            )
        )
        bonus_score = sum(
            phrase in text
            for phrase in (
                "mark",
                "reposition",
                "brief self",
                "next weapon",
                "minor ward",
                "yourself",
            )
        )
        if reaction_score:
            reaction_candidates.append((reaction_score, row["Spell Name"], row))
        if bonus_score and row["Damage"].strip() == "":
            bonus_candidates.append((bonus_score, row["Spell Name"], row))

    for _, _, row in sorted(reaction_candidates, key=lambda item: (-item[0], item[1]))[
        :17
    ]:
        row["Casting Time"] = "Reaction"
        row["Casting Type"] = "Reaction"
        row["Audit - Action Economy Verdict"] = "Change to Reaction"
    for _, _, row in sorted(bonus_candidates, key=lambda item: (-item[0], item[1]))[
        :20
    ]:
        if row["Casting Time"] == "Action":
            row["Casting Time"] = "Bonus Action"
            row["Casting Type"] = "Bonus Action"
            row["Audit - Action Economy Verdict"] = "Change to Bonus Action"
    for row in rows:
        if not row["Audit - Action Economy Verdict"]:
            row["Audit - Action Economy Verdict"] = (
                "Change to Ritual" if row["Ritual"] == "TRUE" else "Keep Action"
            )
        if row["Casting Time"] == "Reaction" and not row["Trigger"].strip():
            match = re.search(r"(?is)\bwhen\b.+?(?=[.!?](?:\s|$))", row["Description"])
            if match:
                row["Trigger"] = re.sub(r"\s+", " ", match.group(0)).strip()


def finish_audit(row: dict[str, str]) -> None:
    text = text_for(row)
    row["Audit - Resolution Model"] = resolution_model(row)
    classify_damage(row)
    audit_permanent(row)
    if level_number(row["Level"]) == 0 or "at higher levels" in text:
        row["Audit - Upcasting Verdict"] = "No Upcast Needed"
    elif row["Damage"].strip():
        row["Audit - Upcasting Verdict"] = "Add Damage Scaling"
    else:
        row["Audit - Upcasting Verdict"] = "Needs Manual Review"

    review_reasons = []
    if row["Spell Name"].strip() in OUTLIERS:
        review_reasons.append("named damage outlier")
    if row["Audit - Damage Verdict"] == "Needs Manual Review":
        review_reasons.append("unclear damage")
    if row["Audit - Permanent Effect Verdict"] != "Safe":
        review_reasons.append("permanent effect")
    if level_number(row["Level"]) >= 6 and any(
        name in class_list(row["Class"]) for name in ("Paladin", "Ranger")
    ):
        review_reasons.append("high-level half-caster access")
    row["Audit - Overall Balance Verdict"] = (
        "Needs Manual Review" if review_reasons else "Acceptable"
    )
    changes = []
    if row["Audit - Cantrip Decision"] == "Promote to 1st-level":
        changes.append("Promoted from cantrip to 1st level")
    if row["Audit - Suggested Class Additions"]:
        changes.append(f"Added {row['Audit - Suggested Class Additions']} access")
    if row["Audit - Suggested Class Removals"]:
        changes.append(f"Removed {row['Audit - Suggested Class Removals']} access")
    if row["Audit - Action Economy Verdict"].startswith("Change"):
        changes.append(
            row["Audit - Action Economy Verdict"].removeprefix("Change to ")
            + " casting"
        )
    changes.extend(f"Review {reason}" for reason in review_reasons)
    row["Audit - Recommended Change Summary"] = (
        "; ".join(changes) or "No further change recommended."
    )


def distributions(rows: list[dict[str, str]]) -> dict[str, Counter[str]]:
    return {
        "level": Counter(row["Level"] for row in rows),
        "school": Counter(row["School"] for row in rows),
        "class": Counter(
            class_name for row in rows for class_name in class_list(row["Class"])
        ),
        "casting": Counter(row["Casting Time"] for row in rows),
    }


def table(counter: Counter[str]) -> str:
    lines = ["| Value | Count |", "|---|---:|"]
    lines.extend(f"| {name} | {count} |" for name, count in sorted(counter.items()))
    return "\n".join(lines)


def class_level_table(rows: list[dict[str, str]]) -> str:
    classes = list(CLASS_LEVEL_TARGETS)
    levels = [
        "0-Cantrip",
        "1st-level",
        "2nd-level",
        "3rd-level",
        "4th-level",
        "5th-level",
        "6th-level",
        "7th-level",
        "8th-level",
        "9th-level",
    ]
    lines = [
        "| Level | " + " | ".join(classes) + " |",
        "|---|" + "|".join("---:" for _ in classes) + "|",
    ]
    for level in levels:
        counts = [
            sum(
                class_name in class_list(row["Class"])
                for row in rows
                if normalize_level(row["Level"]) == level
            )
            for class_name in classes
        ]
        lines.append(
            f"| {level} | " + " | ".join(str(count) for count in counts) + " |"
        )
    return "\n".join(lines)


def write_report(
    path: Path,
    before: list[dict[str, str]],
    after: list[dict[str, str]],
) -> None:
    before_dist = distributions(before)
    after_dist = distributions(after)
    promoted = sum(
        row["Audit - Cantrip Decision"] == "Promote to 1st-level" for row in after
    )
    manual = [
        row
        for row in after
        if row["Audit - Overall Balance Verdict"] == "Needs Manual Review"
    ]
    report = f"""# Orimond Spell Compendium Rebalance Report

## Summary

- Spells processed: {len(after)}
- Cantrips promoted to 1st level: {promoted}
- Saving throws populated: {sum(bool(row["Saving Throw"].strip()) for row in after)}
- Damage types populated: {sum(bool(row["Damage Type"].strip()) for row in after)}
- Conditions populated: {sum(bool(row["Condition"].strip()) for row in after)}
- Ritual spells: {sum(row["Ritual"] == "TRUE" for row in after)}
- Techno Magic spells: {sum(row["Techno Magic"] == "TRUE" for row in after)}
- Spells still requiring manual review: {len(manual)}

The rebalance uses the original `Class` column. `New Class` was preserved but not
used for balance decisions. Mechanical text was not silently rewritten; uncertain
or story-scale effects remain marked for manual review.

## Acceptance Checks

- Cantrip count: {after_dist["level"].get("0-Cantrip", 0)} (target 45-60)
- Damage rows missing a damage type: {sum(bool(row["Damage"].strip()) and not row["Damage Type"].strip() for row in after)}
- Save-based rows missing Success or Fail: {sum(bool(row["Saving Throw"].strip()) and (not row["Success"].strip() or not row["Fail"].strip()) for row in after)}
- Reaction spells missing a trigger: {sum(row["Casting Time"] == "Reaction" and not row["Trigger"].strip() for row in after)}
- Sorcerer access: {after_dist["class"].get("Sorcerer", 0)} (target 120-160)
- Druid access: {after_dist["class"].get("Druid", 0)} (target 80-110)
- Artificer access: {after_dist["class"].get("Artificer", 0)} (target 50-80)
- Ranger access: {after_dist["class"].get("Ranger", 0)} (target 35-60)

## Level Distribution Before

{table(before_dist["level"])}

## Level Distribution After

{table(after_dist["level"])}

## School Distribution Before

{table(before_dist["school"])}

## School Distribution After

{table(after_dist["school"])}

## Original Class Access Before

{table(before_dist["class"])}

## Original Class Access After

{table(after_dist["class"])}

## Original Class Access by Level Before

{class_level_table(before)}

## Original Class Access by Level After

{class_level_table(after)}

## Casting Time Before

{table(before_dist["casting"])}

## Casting Time After

{table(after_dist["casting"])}

## Manual Review

| Spell | Level | Reason |
|---|---|---|
"""
    for row in manual:
        reason = row["Audit - Recommended Change Summary"].replace("|", "/")
        report += f"| {row['Spell Name']} | {row['Level']} | {reason} |\n"
    path.write_text(report, encoding="utf-8")


def rebalance(
    input_path: Path,
    output_path: Path,
    audit_path: Path,
    report_path: Path,
) -> None:
    with input_path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or [])
        original = [dict(row) for row in reader]
    rows = [dict(row) for row in original]
    for row in rows:
        for column in AUDIT_COLUMNS:
            row[column] = ""
        normalize_row(row)
        fill_metadata(row)
        set_concentration(row)
        row["Techno Magic"] = (
            "TRUE"
            if any(contains_keyword(text_for(row), word) for word in TECHNO_WORDS)
            else "FALSE"
        )

    assign_rituals(rows)
    rebalance_cantrips(rows)
    rebalance_schools(rows)
    rebalance_classes(rows)
    rebalance_action_economy(rows)
    for row in rows:
        finish_audit(row)

    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames + AUDIT_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)
    with audit_path.open("w", newline="", encoding="utf-8") as handle:
        audit_fieldnames = ["Spell Name", *AUDIT_COLUMNS]
        writer = csv.DictWriter(
            handle,
            fieldnames=audit_fieldnames,
            extrasaction="ignore",
        )
        writer.writeheader()
        writer.writerows(rows)
    write_report(report_path, original, rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "input", type=Path, nargs="?", default=Path("Orimond - Spells.csv")
    )
    parser.add_argument(
        "--output", type=Path, default=Path("Orimond - Spells.rebalanced.csv")
    )
    parser.add_argument(
        "--audit", type=Path, default=Path("Orimond - Spells.rebalance_audit.csv")
    )
    parser.add_argument(
        "--report", type=Path, default=Path("Orimond - Spells.rebalance_report.md")
    )
    args = parser.parse_args()
    rebalance(args.input, args.output, args.audit, args.report)


if __name__ == "__main__":
    main()
