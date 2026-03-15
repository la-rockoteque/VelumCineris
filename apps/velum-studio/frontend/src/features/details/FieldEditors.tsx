import { useMemo } from "react";
import { styled } from "app/styletron";

import {
  BooleanField,
  ComponentsField,
  DelimitedListField,
  HitDiceField,
  LongTextField,
  MultiSelectField,
  NamedTableField,
  NumberField,
  SelectField,
  StatWithModifierField,
  TextField,
} from "shared/fields";
import { findRowKeyByNormalized, isMonsterSheet, isSpellSheet } from "shared/utils/fields";
import { dedupePreserveCase, normalizeKey, parseDelimitedList, toBoolean } from "shared/utils/text";

interface FieldEditorProps {
  sheet: string;
  fieldName: string;
  value: unknown;
  rowData: Record<string, unknown>;
  validationOptions: string[];
  validationCatalogByField: Record<string, { values: string[] }>;
  validationCatalogBySheet: Record<string, Record<string, string[]>>;
  onFieldChange: (fieldName: string, next: unknown) => void;
  onRowDataPatch: (patch: Record<string, unknown>) => void;
}

function textValue(value: unknown): string {
  if (value == null) {
    return "";
  }
  return String(value);
}

function isBooleanish(fieldName: string, value: string): boolean {
  const normalized = normalizeKey(fieldName);
  if (["ritual", "concentration", "upto", "technomagic", "bloodpact", "hover", "glide", "jump"].some((item) => normalized.includes(item))) {
    return true;
  }
  const lowered = value.trim().toLowerCase();
  return lowered === "true" || lowered === "false" || lowered === "yes" || lowered === "no";
}

function isNumericish(fieldName: string, value: string): boolean {
  const normalized = normalizeKey(fieldName);
  if (/^-?\d+(\.\d+)?$/.test(value.trim())) {
    return true;
  }
  return [
    "count",
    "number",
    "amount",
    "ac",
    "armorclass",
    "proficiencybonus",
    "passiveperception",
    "speed",
    "rangevalue",
    "distancevalue",
    "durationvalue",
    "dc",
    "cr",
    "xp",
    "level",
    "row",
  ].some((token) => normalized.includes(token));
}

function defaultSkillOptions(validationCatalogByField: Record<string, { values: string[] }>): string[] {
  const defaults = [
    "Acrobatics",
    "Animal Handling",
    "Arcana",
    "Athletics",
    "Deception",
    "History",
    "Insight",
    "Intimidation",
    "Investigation",
    "Medicine",
    "Nature",
    "Perception",
    "Performance",
    "Persuasion",
    "Religion",
    "Sleight of Hand",
    "Stealth",
    "Survival",
  ];
  const dynamic = validationCatalogByField[normalizeKey("skills")]?.values ?? validationCatalogByField[normalizeKey("skill")]?.values ?? [];
  return dedupePreserveCase([...defaults, ...dynamic]);
}

function defaultMonsterTypeOptions(
  validationCatalogByField: Record<string, { values: string[] }>,
  validationCatalogBySheet: Record<string, Record<string, string[]>>,
): string[] {
  const defaults = [
    "Aberration",
    "Beast",
    "Celestial",
    "Construct",
    "Dragon",
    "Elemental",
    "Fey",
    "Fiend",
    "Giant",
    "Humanoid",
    "Monstrosity",
    "Ooze",
    "Plant",
    "Undead",
  ];

  const dynamicFields = [
    ...(validationCatalogByField[normalizeKey("Monster Type")]?.values ?? []),
    ...(validationCatalogByField[normalizeKey("Creature Type")]?.values ?? []),
  ];

  const dynamicSheets: string[] = [];
  for (const [sheet, columns] of Object.entries(validationCatalogBySheet)) {
    if (!normalizeKey(sheet).includes("monster")) {
      continue;
    }
    for (const [header, values] of Object.entries(columns)) {
      if (!normalizeKey(header).includes("type")) {
        continue;
      }
      dynamicSheets.push(...values);
    }
  }

  return dedupePreserveCase([...defaults, ...dynamicFields, ...dynamicSheets]);
}

function foundryTagOptions(
  validationCatalogByField: Record<string, { values: string[] }>,
  validationCatalogBySheet: Record<string, Record<string, string[]>>,
): string[] {
  const byField = [
    ...(validationCatalogByField[normalizeKey("Foundry Tag")]?.values ?? []),
    ...(validationCatalogByField[normalizeKey("Foundry")]?.values ?? []),
    ...(validationCatalogByField[normalizeKey("Tag")]?.values ?? []),
  ];

  const bySheet: string[] = [];
  for (const [sheet, columns] of Object.entries(validationCatalogBySheet)) {
    if (!normalizeKey(sheet).includes("spellsvalidation")) {
      continue;
    }
    for (const [header, values] of Object.entries(columns)) {
      const normalized = normalizeKey(header);
      if (normalized.includes("foundry") || normalized.includes("tag")) {
        bySheet.push(...values);
      }
    }
  }

  return dedupePreserveCase([...byField, ...bySheet]);
}

function isMonsterAbility(normalized: string): boolean {
  return ["str", "dex", "con", "int", "wis", "cha"].includes(normalized);
}

function isActionLikeField(normalized: string): boolean {
  return (
    normalized === "traits" ||
    normalized.includes("actions") ||
    normalized === "reactions" ||
    normalized === "legendaryaction" ||
    normalized === "legendaryactions" ||
    normalized === "bonusactions" ||
    normalized === "mythicactions"
  );
}

function isXdyValue(value: string): boolean {
  return /^\s*\d+\s*d\s*\d+(?:\s*[+-]\s*\d+)?\s*$/i.test(value);
}

export function FieldEditor(props: FieldEditorProps) {
  const raw = textValue(props.value);
  const normalized = normalizeKey(props.fieldName);
  const spell = isSpellSheet(props.sheet);
  const monster = isMonsterSheet(props.sheet);

  if (monster && normalized === "name") {
    return <TextField value={raw} onChange={() => undefined} readOnly disabled />;
  }

  if (spell && normalized.includes("component")) {
    return <ComponentsField value={raw} onChange={(next) => props.onFieldChange(props.fieldName, next)} />;
  }

  if (monster && isMonsterAbility(normalized)) {
    return <StatWithModifierField value={raw} onChange={(next) => props.onFieldChange(props.fieldName, next)} />;
  }

  if (spell && normalized === "foundrytag") {
    const options = foundryTagOptions(props.validationCatalogByField, props.validationCatalogBySheet);
    return <MultiSelectField value={raw} options={options} onChange={(next) => props.onFieldChange(props.fieldName, next)} />;
  }

  if (spell && normalized === "skillcheck") {
    const options = defaultSkillOptions(props.validationCatalogByField);
    return <SelectField value={raw} options={options} onChange={(next) => props.onFieldChange(props.fieldName, next)} />;
  }

  if (monster && normalized === "type") {
    const options = defaultMonsterTypeOptions(props.validationCatalogByField, props.validationCatalogBySheet);
    return <SelectField value={raw} options={options} onChange={(next) => props.onFieldChange(props.fieldName, next)} />;
  }

  if (monster && normalized === "skills") {
    const options = defaultSkillOptions(props.validationCatalogByField);
    return <DelimitedListField value={raw} options={options} onChange={(next) => props.onFieldChange(props.fieldName, next)} />;
  }

  if ((monster && normalized === "hitdice") || (normalized.includes("dice") && isXdyValue(raw))) {
    return <HitDiceField value={raw} onChange={(next) => props.onFieldChange(props.fieldName, next)} />;
  }

  if (monster && isActionLikeField(normalized)) {
    return <NamedTableField value={raw} keyLabel="Title" valueLabel="Text" onChange={(next) => props.onFieldChange(props.fieldName, next)} />;
  }

  if (isBooleanish(props.fieldName, raw)) {
    return <BooleanField value={raw} onChange={(next) => props.onFieldChange(props.fieldName, next)} />;
  }

  if (normalized.includes("class") && !normalized.includes("subclass")) {
    const classOptions = props.validationCatalogByField[normalizeKey("classes")]?.values ?? [];
    if (classOptions.length) {
      return <MultiSelectField value={raw} options={classOptions} onChange={(next) => props.onFieldChange(props.fieldName, next)} />;
    }
  }

  if (props.validationOptions.length > 0) {
    const likelyMulti = parseDelimitedList(raw).length > 1;
    if (likelyMulti) {
      return <MultiSelectField value={raw} options={props.validationOptions} onChange={(next) => props.onFieldChange(props.fieldName, next)} />;
    }
    return <SelectField value={raw} options={props.validationOptions} onChange={(next) => props.onFieldChange(props.fieldName, next)} />;
  }

  if (isNumericish(props.fieldName, raw)) {
    return <NumberField value={raw} onChange={(next) => props.onFieldChange(props.fieldName, next)} />;
  }

  if (raw.length > 140 || raw.includes("\n")) {
    return <LongTextField value={raw} rows={5} onChange={(next) => props.onFieldChange(props.fieldName, next)} />;
  }

  return <TextField value={raw} onChange={(next) => props.onFieldChange(props.fieldName, next)} />;
}

export function useEditableTitle(sheet: string, rowData: Record<string, unknown>) {
  const titleKey = useMemo(() => {
    const normalizedName = findRowKeyByNormalized(rowData, ["Name", "Spell Name", "Condition Name", "Feature Name", "Title"]);
    if (isMonsterSheet(sheet)) {
      const bareName = findRowKeyByNormalized(rowData, ["Bare Name"]);
      return bareName || normalizedName;
    }
    return normalizedName;
  }, [rowData, sheet]);

  const title = titleKey ? textValue(rowData[titleKey]) : "";
  return {
    titleKey,
    title,
  };
}

export function syncSpellComponentAbbreviation(rowData: Record<string, unknown>, patch: Record<string, unknown>) {
  const next = { ...rowData, ...patch };
  const componentKey = findRowKeyByNormalized(next, ["Components", "Components ABVR", "Components ABRV"]);
  const abbreviationKey = findRowKeyByNormalized(next, ["Components ABVR", "Components ABRV", "Components Abbreviation"]);
  if (!componentKey || !abbreviationKey) {
    return patch;
  }

  const components = parseDelimitedList(next[componentKey]);
  const mapping: Record<string, string> = {
    verbal: "V",
    somatic: "S",
    material: "M",
    v: "V",
    s: "S",
    m: "M",
  };

  const abbreviated = components
    .map((item) => mapping[normalizeKey(item)] || item)
    .filter(Boolean)
    .join(", ");

  return {
    ...patch,
    [abbreviationKey]: abbreviated,
  };
}

export function syncLinkedSpellFields(sheet: string, fieldName: string, rowData: Record<string, unknown>, value: unknown) {
  if (!isSpellSheet(sheet)) {
    return { [fieldName]: value };
  }

  const normalized = normalizeKey(fieldName);
  if (normalized === "savingthrow") {
    const successKey = findRowKeyByNormalized(rowData, ["Success"]);
    const failKey = findRowKeyByNormalized(rowData, ["Fail"]);
    const patch: Record<string, unknown> = { [fieldName]: value };
    if (!String(value ?? "").trim()) {
      if (successKey) {
        patch[successKey] = "";
      }
      if (failKey) {
        patch[failKey] = "";
      }
    }
    return patch;
  }

  if (normalized === "bloodpact" && !toBoolean(value)) {
    const effectKey = findRowKeyByNormalized(rowData, ["Blood Pact Effect"]);
    if (effectKey) {
      return {
        [fieldName]: value,
        [effectKey]: "",
      };
    }
  }

  return {
    [fieldName]: value,
  };
}
