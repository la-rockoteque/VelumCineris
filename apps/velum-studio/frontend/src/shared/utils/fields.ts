import { normalizeKey } from "./text";

export type FieldBucket =
  | "identity"
  | "description"
  | "classification"
  | "mechanics"
  | "publishing"
  | "additional"
  | "stats"
  | "abilities"
  | "defenses"
  | "speeds"
  | "traits"
  | "actions"
  | "feature"
  | "languages"
  | "proficiencies"
  | "roleplay"
  | "prerequisites"
  | "benefits"
  | "effects"
  | "rules"
  | "media"
  | "lore";

export interface DetailField {
  key: string;
  value: unknown;
  normalized: string;
  raw: string;
}

export type GroupedFields = Record<FieldBucket, DetailField[]>;

export function hasAnyTerm(text: string, terms: string[]): boolean {
  return terms.some((term) => text.includes(term));
}

export function isSpellSheet(sheetName: string): boolean {
  const normalized = normalizeKey(sheetName);
  return normalized === "spell" || normalized === "spells";
}

export function isMonsterSheet(sheetName: string): boolean {
  const normalized = normalizeKey(sheetName);
  return normalized === "monster" || normalized === "monsters";
}

export function isFeatSheet(sheetName: string): boolean {
  const normalized = normalizeKey(sheetName);
  return normalized === "feat" || normalized === "feats";
}

export function isSpeciesSheet(sheetName: string): boolean {
  return normalizeKey(sheetName) === "species";
}

export function isBackgroundSheet(sheetName: string): boolean {
  const normalized = normalizeKey(sheetName);
  return normalized === "background" || normalized === "backgrounds";
}

export function pickItemName(rowData: Record<string, unknown>): string {
  const priority = ["Name", "Spell Name", "Condition Name", "Feature Name", "Title"];
  for (const keyName of priority) {
    const found = findRowKeyByNormalized(rowData, [keyName]);
    if (!found) {
      continue;
    }
    const value = String(rowData[found] ?? "").trim();
    if (value) {
      return value;
    }
  }
  return "";
}

export function findRowKeyByNormalized(rowData: Record<string, unknown>, normalizedKeys: string[]): string {
  const wanted = new Set(normalizedKeys.map((item) => normalizeKey(item)));
  for (const key of Object.keys(rowData)) {
    if (wanted.has(normalizeKey(key))) {
      return key;
    }
  }
  return "";
}

function createEmptyGroups(): GroupedFields {
  return {
    identity: [],
    description: [],
    classification: [],
    mechanics: [],
    publishing: [],
    additional: [],
    stats: [],
    abilities: [],
    defenses: [],
    speeds: [],
    traits: [],
    actions: [],
    feature: [],
    languages: [],
    proficiencies: [],
    roleplay: [],
    prerequisites: [],
    benefits: [],
    effects: [],
    rules: [],
    media: [],
    lore: [],
  };
}

export function groupDetailFields(sheetName: string, rowData: Record<string, unknown>): GroupedFields {
  if (isMonsterSheet(sheetName)) {
    return groupMonsterFields(rowData);
  }
  if (isSpellSheet(sheetName)) {
    return groupSpellFields(rowData);
  }
  if (isSpeciesSheet(sheetName)) {
    return groupSpeciesFields(rowData);
  }
  if (isBackgroundSheet(sheetName)) {
    return groupBackgroundFields(rowData);
  }
  if (isFeatSheet(sheetName)) {
    return groupFeatFields(rowData);
  }

  const groups = createEmptyGroups();
  for (const [key, value] of Object.entries(rowData)) {
    if (key === "_sheet_row") {
      continue;
    }
    const normalized = normalizeKey(key);
    const raw = value == null ? "" : String(value);
    let bucket: FieldBucket = "additional";

    if (hasAnyTerm(normalized, ["name", "title", "source", "type", "subtype", "level", "school", "cr"])) {
      bucket = "identity";
    } else if (hasAnyTerm(normalized, ["description", "details", "summary", "lore", "note", "text"]) || raw.length > 260) {
      bucket = "description";
    } else if (hasAnyTerm(normalized, ["class", "subclass", "species", "language", "tag", "alignment", "size"])) {
      bucket = "classification";
    } else if (hasAnyTerm(normalized, ["distance", "duration", "range", "amount", "time", "component", "damage", "save", "dc"])) {
      bucket = "mechanics";
    } else if (hasAnyTerm(normalized, ["worldanvil", "dndbeyond", "homebrewery", "obsidian", "fivetools", "ddb", "url", "link"])) {
      bucket = "publishing";
    }

    groups[bucket].push({ key, value, normalized, raw });
  }
  return groups;
}

function groupSpellFields(rowData: Record<string, unknown>): GroupedFields {
  const groups = createEmptyGroups();

  for (const [key, value] of Object.entries(rowData)) {
    if (key === "_sheet_row") {
      continue;
    }

    const normalized = normalizeKey(key);
    const raw = value == null ? "" : String(value);

    if (normalized === "alternativeflavor" || normalized === "anomalyeffect") {
      continue;
    }

    if (normalized === "bloodpacteffect") {
      const bloodPactKey = findRowKeyByNormalized(rowData, ["Blood Pact"]);
      const bloodPactValue = bloodPactKey ? rowData[bloodPactKey] : null;
      if (String(bloodPactValue ?? "").toLowerCase() !== "true") {
        continue;
      }
    }

    if (hasAnyTerm(normalized, ["ddb", "worldanvil"]) && !normalized.includes("error")) {
      continue;
    }

    let bucket: FieldBucket = "additional";

    if (hasAnyTerm(normalized, ["spellname", "source", "page", "foundrytag", "tag", "theme", "class", "newclass", "level", "school", "bloodpact", "arcanestrain", "reference"])) {
      bucket = "identity";
    } else if (hasAnyTerm(normalized, ["description", "notes", "clarification", "table", "flavor", "quotes", "quote"])) {
      bucket = "description";
    } else if (hasAnyTerm(normalized, ["range", "duration", "casting", "ritual", "savingthrow", "success", "fail", "skillcheck", "abilitycheck", "trigger", "upto", "concentration", "dc", "damage", "condition", "area", "component", "scaling", "modifier", "technomagic"])) {
      bucket = "mechanics";
    }

    groups[bucket].push({ key, value, normalized, raw });
  }

  return groups;
}

function groupMonsterFields(rowData: Record<string, unknown>): GroupedFields {
  const groups = createEmptyGroups();

  for (const [key, value] of Object.entries(rowData)) {
    if (key === "_sheet_row") {
      continue;
    }

    const normalized = normalizeKey(key);
    if (normalized === "barename" || normalized === "newtype" || normalized === "basedescription" || normalized.startsWith("temp")) {
      continue;
    }

    const raw = value == null ? "" : String(value);
    let bucket: FieldBucket = "additional";

    if (hasAnyTerm(normalized, ["name", "variant", "source", "size", "type", "subtype", "alignment", "cr", "xp"])) {
      bucket = "identity";
    } else if (["str", "dex", "con", "int", "wis", "cha"].includes(normalized)) {
      bucket = "abilities";
    } else if (normalized === "traits") {
      bucket = "traits";
    } else if (hasAnyTerm(normalized, ["actions", "reactions", "bonusactions", "legendaryactions", "legendaryaction", "mythicaction", "mythicactions", "lairaction", "regionaleffect", "regionalfade"])) {
      bucket = "actions";
    } else if (hasAnyTerm(normalized, ["speedwalking", "speedswimming", "speedflying", "speedburrowing", "speedclimbing", "teleport", "jump", "hover", "glide"])) {
      bucket = "speeds";
    } else if (hasAnyTerm(normalized, ["damagevulnerabilities", "damageresistances", "damageimmunities", "conditionimmunities", "weakness", "weaknesses"])) {
      bucket = "defenses";
    } else if (hasAnyTerm(normalized, ["senses", "visionrange", "passiveperception", "languages", "proficiencybonus", "savingthrows", "armorclass", "armortype", "hitdice", "hitpoints", "initiative", "skills"])) {
      bucket = "stats";
    } else if (hasAnyTerm(normalized, ["description", "sidebar", "chargenprompt", "preview"])) {
      bucket = "description";
    }

    groups[bucket].push({ key, value, normalized, raw });
  }

  groups.stats = groups.stats.filter((field) => !field.normalized.endsWith("mod"));
  groups.abilities = groups.abilities.filter((field) => !field.normalized.endsWith("mod"));
  return groups;
}

function groupSpeciesFields(rowData: Record<string, unknown>): GroupedFields {
  const groups = createEmptyGroups();
  for (const [key, value] of Object.entries(rowData)) {
    if (key === "_sheet_row") {
      continue;
    }
    const normalized = normalizeKey(key);
    if (normalized === "score1" || normalized === "score2") {
      continue;
    }
    const raw = value == null ? "" : String(value);
    let bucket: FieldBucket = "additional";

    if (hasAnyTerm(normalized, ["name", "source", "demonym", "tag", "alias", "slogan", "quote", "size"])) {
      bucket = "identity";
    } else if (hasAnyTerm(normalized, ["ability", "score", "walkspeed", "flyspeed", "speed", "vision", "age"])) {
      bucket = "stats";
    } else if (hasAnyTerm(normalized, ["language"])) {
      bucket = "languages";
    } else if (normalized.startsWith("trait")) {
      bucket = "traits";
    } else if (hasAnyTerm(normalized, ["intro", "origin", "appearance", "cultureidentity", "societalroles", "namingconventions", "lifeinorimond", "playstyleroleplaying"])) {
      bucket = "lore";
    } else if (hasAnyTerm(normalized, ["preview", "image", "chargen", "ddb", "wa"])) {
      bucket = "media";
    }

    groups[bucket].push({ key, value, normalized, raw });
  }
  return groups;
}

function groupFeatFields(rowData: Record<string, unknown>): GroupedFields {
  const groups = createEmptyGroups();
  for (const [key, value] of Object.entries(rowData)) {
    if (key === "_sheet_row") {
      continue;
    }
    const normalized = normalizeKey(key);
    const raw = value == null ? "" : String(value);
    let bucket: FieldBucket = "additional";

    if (hasAnyTerm(normalized, ["name", "source", "page", "category", "tag", "feattype"])) {
      bucket = "identity";
    } else if (normalized.startsWith("prerequisite")) {
      bucket = "prerequisites";
    } else if (hasAnyTerm(normalized, ["asi", "grantschoice", "choicecount", "actiontype", "reactiontrigger", "bonusactioncondition", "usagetype", "usageamount", "usagereset", "scalingtype", "scalingvalue"])) {
      bucket = "benefits";
    } else if (hasAnyTerm(normalized, ["grantedspells", "spellcastingability", "savedcformula", "attackbonusformula", "conditionsapplied", "modifiersgranted", "proficienciesgranted", "sensesgranted", "movementgranted"])) {
      bucket = "effects";
    } else if (hasAnyTerm(normalized, ["rulestext", "rulesbullets", "passiveeffects", "activeeffects", "resourceinteraction", "limitations", "designernotes"])) {
      bucket = "rules";
    }

    groups[bucket].push({ key, value, normalized, raw });
  }
  return groups;
}

function groupBackgroundFields(rowData: Record<string, unknown>): GroupedFields {
  const groups = createEmptyGroups();
  for (const [key, value] of Object.entries(rowData)) {
    if (key === "_sheet_row") {
      continue;
    }
    const normalized = normalizeKey(key);
    const raw = value == null ? "" : String(value);
    let bucket: FieldBucket = "additional";

    if (hasAnyTerm(normalized, ["name", "source", "page", "category", "tag"])) {
      bucket = "identity";
    } else if (normalized.startsWith("feature")) {
      bucket = "feature";
    } else if (hasAnyTerm(normalized, ["languagechoice", "languagecount"])) {
      bucket = "languages";
    } else if (hasAnyTerm(normalized, ["skillproficiency", "toolproficiency"])) {
      bucket = "proficiencies";
    } else if (hasAnyTerm(normalized, ["personalitytraits", "ideals", "bonds", "flaws"])) {
      bucket = "roleplay";
    } else if (hasAnyTerm(normalized, ["equipmenttext", "limitations", "designernotes", "goldalternative", "starting"])) {
      bucket = "description";
    }

    groups[bucket].push({ key, value, normalized, raw });
  }
  return groups;
}

export function findPrimaryNameFieldKey(sheetName: string, rowData: Record<string, unknown>): string {
  if (isMonsterSheet(sheetName)) {
    const bareNameKey = findRowKeyByNormalized(rowData, ["Bare Name"]);
    if (bareNameKey) {
      return bareNameKey;
    }
  }
  return findRowKeyByNormalized(rowData, ["Name", "Spell Name", "Condition Name", "Feature Name", "Title"]);
}

export function stripNameFields(sheetName: string, rowData: Record<string, unknown>, groups: GroupedFields): GroupedFields {
  const primary = findPrimaryNameFieldKey(sheetName, rowData);
  if (!primary) {
    return groups;
  }
  const copy: GroupedFields = { ...groups };
  for (const [bucket, fields] of Object.entries(copy) as Array<[FieldBucket, DetailField[]]>) {
    copy[bucket] = fields.filter((field) => field.key !== primary);
  }
  return copy;
}

export function getSectionOrder(sheetName: string): Array<[FieldBucket, string]> {
  if (isSpeciesSheet(sheetName)) {
    return [
      ["identity", "Identifier"],
      ["stats", "Stats"],
      ["languages", "Languages"],
      ["traits", "Traits"],
      ["lore", "Lore"],
      ["media", "Media"],
      ["additional", "Additional"],
    ];
  }
  if (isFeatSheet(sheetName)) {
    return [
      ["identity", "Identifier"],
      ["prerequisites", "Prerequisites"],
      ["benefits", "Benefits"],
      ["effects", "Effects"],
      ["rules", "Rules"],
      ["additional", "Additional"],
    ];
  }
  if (isMonsterSheet(sheetName)) {
    return [
      ["identity", "Identifier"],
      ["stats", "Core Stats"],
      ["abilities", "Abilities"],
      ["defenses", "Defenses"],
      ["speeds", "Speeds"],
      ["traits", "Traits"],
      ["actions", "Actions"],
      ["description", "Description"],
      ["additional", "Additional"],
    ];
  }
  if (isBackgroundSheet(sheetName)) {
    return [
      ["identity", "Identifier"],
      ["feature", "Feature"],
      ["languages", "Languages"],
      ["proficiencies", "Proficiencies"],
      ["roleplay", "Roleplay Tables"],
      ["description", "Description"],
      ["additional", "Additional"],
    ];
  }
  return [
    ["identity", "Identity"],
    ["description", "Description"],
    ["classification", "Classification"],
    ["mechanics", "Mechanics"],
    ["publishing", "Publishing"],
    ["additional", "Additional"],
  ];
}
