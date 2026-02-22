#!/usr/bin/env python3

import re
from pathlib import Path

import pandas as pd


SPECIES_PATH = "assets/Orimond_Species.csv"
APPEARANCE_PATH = "assets/Orimond_Species_Appearance.csv"
MODERN_DIR = Path("assets/art/Species/modern")


def norm(text: str) -> str:
  return re.sub(r"[^a-z0-9]+", "", (text or "").lower())


def is_empty(value) -> bool:
  return value is None or (isinstance(value, str) and value.strip() == "")


def set_if_empty(df, idx, col, value):
  if is_empty(value):
    return False
  if col not in df.columns:
    return False
  if is_empty(df.at[idx, col]):
    df.at[idx, col] = value
    return True
  return False


def extract_height(size_text: str) -> str:
  if not size_text:
    return ""
  # Match ranges like 5'8" to 6'6"
  m = re.search(
    r"(\d)\s?[’']\s?(\d{1,2})\s?[\"”]?\s*(?:to|-|–|—)\s*(\d)\s?[’']\s?(\d{1,2})",
    size_text,
  )
  if m:
    return f"{m.group(1)}'{m.group(2)}\"-{m.group(3)}'{m.group(4)}\""
  return ""


def find_terms(text: str, term_map):
  if not text:
    return ""
  found = []
  lower_text = text.lower()
  for pattern, value in term_map:
    if re.search(pattern, lower_text):
      if value not in found:
        found.append(value)
  return "; ".join(found)


def find_build(text: str) -> str:
  if not text:
    return ""
  build_terms = [
    "slender",
    "lean",
    "wiry",
    "stocky",
    "stout",
    "muscular",
    "hulking",
    "compact",
    "towering",
    "tall",
    "short",
  ]
  lower_text = text.lower()
  for term in build_terms:
    if re.search(rf"\b{re.escape(term)}\b", lower_text):
      return term
  return ""


def extract_eye_count(text: str) -> str:
  if not text:
    return ""
  lower_text = text.lower()
  word_map = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
  }
  m = re.search(r"\b(\d+)\s+eyes\b", lower_text)
  if m:
    return m.group(1)
  m = re.search(r"\b(one|two|three|four|five|six|seven|eight)\s+eyes\b", lower_text)
  if m:
    return word_map[m.group(1)]
  return ""


def extract_ear_type(text: str) -> str:
  if not text:
    return ""
  lower_text = text.lower()
  if re.search(r"\bpointed\s+ears\b", lower_text):
    return "pointed"
  if re.search(r"\belongated\s+ears\b", lower_text):
    return "elongated"
  return ""


def extract_ancestor(origin_text: str, species_names, current_name: str) -> str:
  if not origin_text:
    return ""
  lower_text = origin_text.lower()
  triggers = [
    "descended from",
    "descendants of",
    "descendant of",
    "offspring of",
    "scions of",
  ]
  if not any(t in lower_text for t in triggers):
    return ""

  matches = []
  for candidate in species_names:
    if norm(candidate) == norm(current_name):
      continue
    if re.search(rf"\b{re.escape(candidate)}\b", origin_text, flags=re.IGNORECASE):
      matches.append(candidate)

  if len(matches) == 1:
    return matches[0]
  return ""


def build_modern_refs():
  refs = {}
  if not MODERN_DIR.exists():
    return refs

  for path in MODERN_DIR.glob("*.png"):
    stem = path.stem
    m = re.match(r"^(.*)_(M|F)$", stem, flags=re.IGNORECASE)
    base = m.group(1) if m else stem
    key = norm(base)
    refs.setdefault(key, []).append(str(path))
  return refs


def main():
  species_df = pd.read_csv(SPECIES_PATH, dtype=str, keep_default_na=False)
  appearance_df = pd.read_csv(APPEARANCE_PATH, dtype=str, keep_default_na=False)

  species_by_norm = {norm(row["Name"]): row for _, row in species_df.iterrows()}
  all_species_names = [row["Name"] for _, row in species_df.iterrows()]

  modern_refs = build_modern_refs()

  defensive_map = [
    (r"\bhorn(s)?\b", "horns"),
    (r"\btusk(s)?\b", "tusks"),
    (r"\bantler(s)?\b", "antlers"),
    (r"\bspine(s)?\b", "spines"),
    (r"\bquill(s)?\b", "quills"),
    (r"\bspike(s)?\b", "spikes"),
    (r"\bcarapace\b|\bshell\b", "carapace"),
  ]
  skin_texture_map = [
    (r"\bmatte\b", "matte"),
    (r"\bsmooth\b", "smooth"),
    (r"\bleathery\b", "leathery"),
    (r"\bscaled\b|\bscales\b", "scaled"),
    (r"\bfurred\b|\bfurry\b", "furred"),
    (r"\bfeathered\b|\bfeathers\b", "feathered"),
    (r"\bcoarse\b", "coarse"),
    (r"\bridged\b", "ridged"),
    (r"\btextured\b|\bmicro-textured\b", "textured"),
  ]
  markings_map = [
    (r"\bfreckle(s)?\b", "freckles"),
    (r"\bspeckle(s)?\b", "speckles"),
    (r"\bmottl(ed|ing)\b", "mottling"),
    (r"\bstripe(s)?\b", "stripes"),
    (r"\bspot(s)?\b", "spots"),
    (r"\bstreak(s)?\b", "streaks"),
  ]
  eye_shape_map = [
    (r"\balmond-shaped\b", "almond"),
    (r"\bslit\b", "slit"),
    (r"\bround\b", "round"),
    (r"\bnarrow\b", "narrow"),
  ]
  hair_texture_map = [
    (r"\bwiry\b", "wiry"),
    (r"\bcoarse\b", "coarse"),
    (r"\bsilky\b", "silky"),
    (r"\bcurly\b", "curly"),
    (r"\bstraight\b", "straight"),
    (r"\bwavy\b", "wavy"),
    (r"\bvoluminous\b", "voluminous"),
    (r"\bthick\b", "thick"),
  ]

  for idx, row in appearance_df.iterrows():
    name = row.get("Name", "")
    if is_empty(name):
      continue

    species = species_by_norm.get(norm(name))
    if species is None:
      continue

    appearance_text = (species.get("Appearance", "") or "").strip()
    size_text = (species.get("Size", "") or "").strip()
    origin_text = (species.get("Origin", "") or "").strip()

    # Direct field mappings
    set_if_empty(appearance_df, idx, "Demonym", species.get("Demonym", ""))
    size_cat = species.get("Size ABRV", "") or ""
    if is_empty(size_cat):
      size_cat = ""
      if re.search(r"\bSmall\b", size_text, flags=re.IGNORECASE):
        size_cat = "Small"
      elif re.search(r"\bMedium\b", size_text, flags=re.IGNORECASE):
        size_cat = "Medium"
      elif re.search(r"\bLarge\b", size_text, flags=re.IGNORECASE):
        size_cat = "Large"
    set_if_empty(appearance_df, idx, "Size Category", size_cat)
    set_if_empty(appearance_df, idx, "Lifespan Average", species.get("Age", ""))
    set_if_empty(appearance_df, idx, "Secondary Vision Traits", species.get("Vision", ""))

    # Ancestor extraction from explicit lineage phrasing
    ancestor = extract_ancestor(origin_text, all_species_names, name)
    set_if_empty(appearance_df, idx, "Ancestor", ancestor)

    # Height/build from Size text
    set_if_empty(appearance_df, idx, "Average Height", extract_height(size_text))
    set_if_empty(appearance_df, idx, "Average Build", find_build(size_text))

    # Appearance-derived traits
    set_if_empty(
      appearance_df,
      idx,
      "Defensive Growth",
      find_terms(appearance_text, defensive_map),
    )
    set_if_empty(
      appearance_df,
      idx,
      "Skin Texture",
      find_terms(appearance_text, skin_texture_map),
    )
    set_if_empty(
      appearance_df,
      idx,
      "Markings",
      find_terms(appearance_text, markings_map),
    )
    set_if_empty(
      appearance_df,
      idx,
      "Eye Shape",
      find_terms(appearance_text, eye_shape_map),
    )
    set_if_empty(appearance_df, idx, "Eye Count", extract_eye_count(appearance_text))
    set_if_empty(appearance_df, idx, "Ear Type", extract_ear_type(appearance_text))

    # Hair presence/texture (only if "hair" explicitly mentioned)
    if "hair" in appearance_text.lower():
      set_if_empty(appearance_df, idx, "Hair Presence", "present")
      set_if_empty(
        appearance_df,
        idx,
        "Hair Texture",
        find_terms(appearance_text, hair_texture_map),
      )

    # Posture if explicitly noted
    if re.search(r"\bhunched\b|\bstooped\b", appearance_text, flags=re.IGNORECASE):
      set_if_empty(appearance_df, idx, "Posture", "hunched")

    # References to modern images (filenames only, no visual inference)
    if is_empty(row.get("References Species", "")):
      key = norm(name)
      refs = modern_refs.get(key, [])
      if not refs and key.endswith("s"):
        refs = modern_refs.get(key[:-1], [])
      if refs:
        set_if_empty(
          appearance_df,
          idx,
          "References Species",
          "; ".join(sorted(refs)),
        )

  appearance_df.to_csv(APPEARANCE_PATH, index=False)


if __name__ == "__main__":
  main()
