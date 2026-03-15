import { normalizeKey } from "./text";

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
