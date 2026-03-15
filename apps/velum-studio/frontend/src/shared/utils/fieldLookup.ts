import type { DetailField, FieldBucket, GroupedFields } from "./fieldTypes";
import { isMonsterSheet } from "./fieldSheets";
import { normalizeKey } from "./text";

export function findRowKeyByNormalized(
  rowData: Record<string, unknown>,
  normalizedKeys: string[],
): string {
  const wanted = new Set(normalizedKeys.map((item) => normalizeKey(item)));
  for (const key of Object.keys(rowData)) {
    if (wanted.has(normalizeKey(key))) {
      return key;
    }
  }
  return "";
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

export function findPrimaryNameFieldKey(
  sheetName: string,
  rowData: Record<string, unknown>,
): string {
  if (isMonsterSheet(sheetName)) {
    const bareNameKey = findRowKeyByNormalized(rowData, ["Bare Name"]);
    if (bareNameKey) {
      return bareNameKey;
    }
  }
  return findRowKeyByNormalized(rowData, [
    "Name",
    "Spell Name",
    "Condition Name",
    "Feature Name",
    "Title",
  ]);
}

export function stripNameFields(
  sheetName: string,
  rowData: Record<string, unknown>,
  groups: GroupedFields,
): GroupedFields {
  const primary = findPrimaryNameFieldKey(sheetName, rowData);
  if (!primary) {
    return groups;
  }

  const copy: GroupedFields = { ...groups };
  for (const [bucket, fields] of Object.entries(copy) as Array<
    [FieldBucket, DetailField[]]
  >) {
    copy[bucket] = fields.filter((field) => field.key !== primary);
  }
  return copy;
}
