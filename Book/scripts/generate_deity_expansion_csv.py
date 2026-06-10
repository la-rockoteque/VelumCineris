from __future__ import annotations

import ast
import csv
import json
import re
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
TARGETS_PATH = Path("/tmp/deity_expansion_targets.json")
OUTPUT_PATH = REPO_ROOT / "Book" / "core" / "markdown" / "deity_content_expansion_proposals.csv"


def clean(value: Any, default: str = "") -> str:
    text = str(value or "").strip()
    return text if text and text != "[]" else default


def domains(value: str) -> list[str]:
    if not value:
        return []
    try:
        parsed = ast.literal_eval(value)
    except (SyntaxError, ValueError):
        parsed = re.split(r"[;,]", value)
    if not isinstance(parsed, list):
        parsed = [parsed]
    return [clean(item) for item in parsed if clean(item)]


def sentence(text: str) -> str:
    match = re.search(r".+?[.!?](?:\s|$)", text, re.DOTALL)
    return clean(match.group(0) if match else text)


def join_naturally(values: list[str], fallback: str) -> str:
    if not values:
        return fallback
    if len(values) == 1:
        return values[0]
    return ", ".join(values[:-1]) + f", and {values[-1]}"


def proposed_description(entry: dict[str, str]) -> str:
    original = clean(entry["description"])
    if len(original) >= 500:
        return original

    name = entry["name"]
    epithet = clean(entry["epithet"], "an old divine power")
    plane = clean(entry["plane"], "the hidden reaches beyond Orimond")
    pantheon = clean(entry["pantheon"])
    alignment = clean(entry["alignment"])
    domain_text = join_naturally(domains(entry["domains"]), "an uncertain divine purpose")
    symbol = clean(entry["symbol"])
    followers = clean(entry["followers"], "travelers, household devotees, and local keepers of old rites")

    if original:
        opening = original
    else:
        opening = (
            f"{name}, known in surviving traditions as {epithet}, is associated with "
            f"{domain_text}. Accounts place this power in {plane}, though theologians "
            f"disagree on whether that realm is a dwelling, a prison, or simply the "
            f"closest mortal metaphor for its presence."
        )

    symbol_text = (
        f" The faithful recognize {name} through {symbol}, an emblem carried during "
        "private vows and displayed only when divine attention is deliberately invited."
        if symbol
        else
        f" No single symbol of {name} is accepted everywhere; each cult preserves a "
        "different sign and insists that rival forms misunderstand the deity."
    )
    standing = (
        f"Within {pantheon}, {name} is commonly interpreted through {alignment or 'an uncertain moral nature'}."
        if pantheon
        else (
            f"No universally accepted pantheon claims {name}, and surviving traditions "
            f"assign the deity {alignment or 'no settled moral nature'}."
        )
    )
    return (
        f"{opening}\n\n"
        f"{standing} "
        f"That judgment is not simple praise or condemnation: worshippers understand "
        f"the deity as a power whose gifts become dangerous when pursued without restraint."
        f"{symbol_text}\n\n"
        f"Devotion is most common among {followers}. Their prayers ask less for effortless "
        f"victory than for the resolve to endure the consequences of choosing {name}'s path. "
        f"Shrines tend to be practical places where offerings are used, shared, repaired, "
        f"or returned to the world rather than left untouched."
    )


def proposed_lore(entry: dict[str, str], index: int) -> str:
    original = clean(entry["lore"])
    name = entry["name"]
    epithet = clean(entry["epithet"], "the unnamed power")
    plane = clean(entry["plane"], "an uncertain realm")
    pantheon = clean(entry["pantheon"], "no settled pantheon")
    symbol = clean(entry["symbol"], "a sign that changes between traditions")
    domain_values = domains(entry["domains"])
    domain_text = join_naturally(domain_values, "the deity's uncertain concerns")
    description_anchor = sentence(clean(entry["description"]))
    quote = clean(entry["quote"])

    openings = [
        (
            f"The oldest surviving account of {name} is not a genealogy but a warning. "
            f"It claims that mortals first recognized {epithet} when an ordinary choice "
            "continued to shape events long after every witness had died."
        ),
        (
            f"Priests disagree about when {name} entered the world. One tradition says "
            f"{epithet} emerged from {plane}; another insists the deity was already present "
            "and merely became visible when mortals learned the correct name."
        ),
        (
            f"A disputed hymn places {name} at the edge of an ancient catastrophe. "
            f"The hymn never states whether {epithet} caused the disaster, prevented a "
            "greater one, or simply ensured that something meaningful survived."
        ),
        (
            f"Among the stories attached to {pantheon}, the tale of {name} is told most "
            "often in unfinished form. Each temple supplies a different ending, turning "
            f"{epithet} into judge, witness, tempter, or reluctant protector."
        ),
    ]
    rites = [
        (
            f"A common rite dedicated to {name} is called the Keeping of the Sign. "
            f"Devotees place {symbol} beside an object connected to a difficult promise, "
            "then leave both untouched until the promise is fulfilled or openly abandoned."
        ),
        (
            f"At seasonal observances, worshippers invoke {name} through acts connected to "
            f"{domain_text}. The rite ends with each participant naming one consequence "
            "they are willing to accept and one cost they refuse to impose on another."
        ),
        (
            f"Small cults preserve a vigil known as the Unanswered Offering. A token marked "
            f"with {symbol} is given without a spoken request. Whatever follows is interpreted "
            "not as a reward, but as evidence of what the worshipper truly desired."
        ),
        (
            f"Pilgrims seeking {name} carry no standardized prayer. Instead they perform a "
            f"task associated with {domain_text}, repeat it until its purpose changes, and "
            "record the moment duty becomes devotion or devotion becomes obsession."
        ),
    ]
    disputes = [
        (
            f"Theologians remain divided over {name}'s place within {pantheon}. Some describe "
            "the deity as a necessary counterweight; others argue that this interpretation "
            "was created by later institutions seeking divine support for mortal customs."
        ),
        (
            f"Stories of {name} rarely agree on motive. Acts praised as mercy in one region "
            "are remembered as manipulation in another. This contradiction is central to the "
            "faith, whose teachers warn that divine purpose does not erase mortal suffering."
        ),
        (
            f"Several forbidden commentaries claim that {name}'s apparent domain is only a "
            "surface expression of a deeper concern. Their authors vanished or recanted, "
            "leaving fragments that continue to inspire rival cults and dangerous expeditions."
        ),
        (
            f"Even devoted priests caution against treating {name} as predictable. The deity's "
            "most famous blessings often solve the immediate crisis while creating a harder "
            "question for the next generation to answer."
        ),
    ]

    anchor = (
        f"\n\nLater commentators begin from a single accepted claim: {description_anchor}"
        if description_anchor
        else ""
    )
    quote_note = (
        f"\n\nThe saying most often repeated by initiates is: “{quote}” Priests treat it "
        "as a test rather than a command, asking what kind of person would find comfort in it."
        if quote and len(quote) < 220
        else ""
    )
    expansion = (
        f"{openings[index % len(openings)]}{anchor}\n\n"
        f"{rites[(index // 2) % len(rites)]}\n\n"
        f"{disputes[(index // 3) % len(disputes)]}{quote_note}"
    )
    return f"{original}\n\n{expansion}".strip() if original else expansion


def main() -> None:
    targets = json.loads(TARGETS_PATH.read_text(encoding="utf-8"))
    rows = []
    for index, entry in enumerate(targets):
        original_description = clean(entry["description"])
        original_lore = clean(entry["lore"])
        description = proposed_description(entry)
        lore = proposed_lore(entry, index)
        reasons = []
        if len(original_description) < 500:
            reasons.append(
                "Description missing" if not original_description else "Description under 500 characters"
            )
        if len(original_lore) < 250:
            reasons.append("Lore missing" if not original_lore else "Lore under 250 characters")
        if not any(
            clean(entry[field])
            for field in ("epithet", "pantheon", "domains", "plane", "alignment", "symbol")
        ):
            reasons.append("Speculative draft: no supporting metadata found")
        rows.append(
            {
                "Name": entry["name"],
                "Original Description": original_description,
                "Proposed Description": description,
                "Original Lore": original_lore,
                "Proposed Lore": lore,
                "Change Reason": "; ".join(reasons),
            }
        )

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open("w", encoding="utf-8", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(OUTPUT_PATH)


if __name__ == "__main__":
    main()
