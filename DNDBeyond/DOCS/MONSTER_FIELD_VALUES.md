# Monster Form Field Values

Source of truth: `requests/monsters.create.response.html` (monster creator form).

## Required Enum Fields
These are used by `convert_monster_to_ddb()` to map common inputs to D&D Beyond IDs.

### Stat Block Type
- `2014` -> `0`
- `2024` -> `1`

### Monster Type
- `aberration` -> `1`
- `beast` -> `2`
- `celestial` -> `3`
- `construct` -> `4`
- `dragon` -> `6`
- `elemental` -> `7`
- `fey` -> `8`
- `fiend` -> `9`
- `giant` -> `10`
- `humanoid` -> `11`
- `monstrosity` -> `13`
- `ooze` -> `14`
- `plant` -> `15`
- `undead` -> `16`
- `unknown` -> `17`

### Size
- `tiny` -> `2`
- `small` -> `3`
- `medium` -> `4`
- `large` -> `5`
- `huge` -> `6`
- `gargantuan` -> `7`
- `medium or small` -> `10`

### Alignment
- `lawful good` -> `1`
- `neutral good` -> `2`
- `chaotic good` -> `3`
- `lawful neutral` -> `4`
- `neutral` -> `5`
- `chaotic neutral` -> `6`
- `lawful evil` -> `7`
- `neutral evil` -> `8`
- `chaotic evil` -> `9`
- `unaligned` -> `10`
- `any alignment` -> `11`
- `any good alignment` -> `14`
- `any evil alignment` -> `13`
- `any lawful alignment` -> `16`
- `any chaotic alignment` -> `15`
- `any neutral alignment` -> `29`
- `any non-good alignment` -> `18`
- `any non-lawful alignment` -> `19`
- `any non-chaotic alignment` -> `30`
- `typically lawful good` -> `22`
- `typically neutral good` -> `21`
- `typically chaotic good` -> `25`
- `typically lawful neutral` -> `28`
- `typically neutral` -> `26`
- `typically chaotic neutral` -> `20`
- `typically lawful evil` -> `27`
- `typically neutral evil` -> `24`
- `typically chaotic evil` -> `23`

### Challenge Rating
- `0` -> `1`
- `1/8` -> `2`
- `1/4` -> `3`
- `1/2` -> `4`
- `1` -> `5`
- `2` -> `6`
- `3` -> `7`
- `4` -> `8`
- `5` -> `9`
- `6` -> `10`
- `7` -> `11`
- `8` -> `12`
- `9` -> `13`
- `10` -> `14`
- `11` -> `15`
- `12` -> `16`
- `13` -> `17`
- `14` -> `18`
- `15` -> `19`
- `16` -> `20`
- `17` -> `21`
- `18` -> `22`
- `19` -> `23`
- `20` -> `24`
- `21` -> `25`
- `22` -> `26`
- `23` -> `27`
- `24` -> `29`
- `25` -> `30`
- `26` -> `31`
- `27` -> `32`
- `28` -> `33`
- `29` -> `34`
- `30` -> `35`

### Hit Dice
- `d4` -> `4`
- `d6` -> `6`
- `d8` -> `8`
- `d10` -> `10`
- `d12` -> `12`
- `d20` -> `20`

### Saving Throws
- `str` -> `1`
- `dex` -> `2`
- `con` -> `3`
- `int` -> `4`
- `wis` -> `5`
- `cha` -> `6`

## Hashed Field Names (Stats + Saves)
These IDs are required by the monster form; they are stable in the captured HTML.

- `initiative_bonus` -> `fb6b1dd00d26bfc516f55d8bafdb2397b`
- `str_score` -> `f033aeb36a3b272c382e6727aa232ddf4`
- `dex_score` -> `f11255511cc5507bf3490e72951cd16c2`
- `con_score` -> `fc552a9b8ad173bc3d4f37d3378ef1b6c`
- `int_score` -> `f50bea7c52c2892ada54f1c35c3e5842b`
- `wis_score` -> `fa5fbba63e5834bf995e73c7524086cc6`
- `cha_score` -> `f0b661270490219283e84bfee50d77a25`
- `str_save_bonus` -> `fa168b83124d247d452f6a978e2f1dfbc`
- `dex_save_bonus` -> `f3dd3def85875c9a4c8f883e07c616e8d`
- `con_save_bonus` -> `fd0d9c1742334f9dfb15fd7599d171fba`
- `int_save_bonus` -> `f0a588408093e39a5ed7514324f1edf49`
- `wis_save_bonus` -> `f6678b290486f65432188f3237545e354`
- `cha_save_bonus` -> `f2a54f7938f06cb51a6f6982e5ca80536`
- `avatar_small` -> `f0fcf1b0a2147f857157d81be3e6e0c99`
- `avatar_large` -> `ffc6259e7fa1df63a60af363c86678dcf`

## Large Select Lists (IDs Required)
These lists are large and should be sourced from the HTML when needed:
- `monster-sub-type`
- `swarm-monster`
- `damage-adjustment`
- `monster-tags-public`

Quick extraction example (run locally):

```python
import re
from pathlib import Path

html = Path("requests/monsters.create.response.html").read_text(encoding="utf-8")
select_re = re.compile(r'<select[^>]*name="([^"]+)"[^>]*>(.*?)</select>', re.S | re.I)
option_re = re.compile(r'<option[^>]*value="([^"]*)"[^>]*>(.*?)</option>', re.S | re.I)

for name, inner in select_re.findall(html):
    if name in {"monster-sub-type", "swarm-monster", "damage-adjustment", "monster-tags-public"}:
        print(name)
        for value, label in option_re.findall(inner):
            label = re.sub(r"\\s+", " ", re.sub(r"<[^>]+>", "", label)).strip()
            print(value, label)
        print()
```
