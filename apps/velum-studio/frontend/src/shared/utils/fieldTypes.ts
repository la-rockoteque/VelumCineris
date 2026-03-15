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

export function createEmptyGroups(): GroupedFields {
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
