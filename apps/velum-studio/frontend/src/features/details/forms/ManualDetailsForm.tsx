import { FieldEditor } from "features/details/FieldEditors";
import type { CSSProperties } from "react";
import { Section } from "shared/library";
import { findPrimaryNameFieldKey, findRowKeyByNormalized } from "shared/utils/fields";
import { asText, normalizeKey } from "shared/utils/text";

import type { ItemDetailsFormProps, ManualFieldConfig, ManualSectionConfig } from "./types";

interface AbbreviationEntry {
  key: string;
  normalized: string;
  value: unknown;
}

function isAbbreviationField(normalizedField: string): boolean {
  return ["abbreviation", "abbr", "abrv", "abvr"].some((token) => normalizedField.includes(token));
}

function abbreviationRootKey(normalizedField: string): string {
  return normalizedField.replace(/abbreviation|abbr|abrv|abvr/g, "");
}

function consumeMatchingAbbreviation(map: Map<string, AbbreviationEntry>, fieldRoot: string): AbbreviationEntry | null {
  if (!fieldRoot) {
    return null;
  }
  if (map.has(fieldRoot)) {
    const item = map.get(fieldRoot) || null;
    map.delete(fieldRoot);
    return item;
  }

  for (const [root, item] of map.entries()) {
    if (!root) {
      continue;
    }
    if (fieldRoot.includes(root) || root.includes(fieldRoot)) {
      map.delete(root);
      return item;
    }
  }

  return null;
}

function resolveValidationOptions(
  fieldName: string,
  catalog: ItemDetailsFormProps["validationCatalog"],
  lookupFieldOptions: ItemDetailsFormProps["lookupFieldOptions"],
): string[] {
  const direct = catalog?.options_by_field?.[normalizeKey(fieldName)]?.values;
  if (Array.isArray(direct) && direct.length) {
    return direct;
  }
  return lookupFieldOptions(fieldName);
}

function resolveSpan(field: ManualFieldConfig): string {
  if (field.span === "full") {
    return "field-span-full";
  }
  if (typeof field.span === "number" && Number.isFinite(field.span) && field.span > 0) {
    return "";
  }
  return "";
}

function resolveFieldKey(rowData: Record<string, unknown>, wanted: string): string {
  return findRowKeyByNormalized(rowData, [wanted]);
}

function fieldGridStyle(field: ManualFieldConfig): CSSProperties | undefined {
  if (field.span === "full") {
    return undefined;
  }
  if (typeof field.span === "number" && Number.isFinite(field.span) && field.span > 0) {
    return { gridColumn: `span ${Math.min(12, Math.max(1, Math.floor(field.span)))}` };
  }
  return undefined;
}

function buildAbbreviationMap(rowData: Record<string, unknown>) {
  const abbreviationByRoot = new Map<string, AbbreviationEntry>();

  for (const [key, value] of Object.entries(rowData)) {
    if (key === "_sheet_row") {
      continue;
    }
    const normalized = normalizeKey(key);
    if (!isAbbreviationField(normalized)) {
      continue;
    }
    const root = abbreviationRootKey(normalized);
    if (!root || abbreviationByRoot.has(root)) {
      continue;
    }
    abbreviationByRoot.set(root, { key, normalized, value });
  }

  return abbreviationByRoot;
}

function toConfig(field: string): ManualFieldConfig {
  return { field };
}

export function ManualDetailsForm(props: ItemDetailsFormProps & { schema: ManualSectionConfig[] }) {
  const abbreviationByRoot = buildAbbreviationMap(props.rowData);
  const used = new Set<string>();
  const primaryNameKey = findPrimaryNameFieldKey(props.sheet, props.rowData);

  return (
    <>
      {props.schema.map((section) => {
        const configured = section.fields.map((field) => {
          const config = toConfig(field.field);
          config.span = field.span;
          return config;
        });

        if (section.includeRemaining) {
          for (const key of Object.keys(props.rowData)) {
            if (key === "_sheet_row") {
              continue;
            }
            if (key === primaryNameKey) {
              continue;
            }
            if (isAbbreviationField(normalizeKey(key))) {
              continue;
            }
            if (used.has(key)) {
              continue;
            }
            configured.push({ field: key });
          }
        }

        const resolved = configured
          .map((field) => {
            const fieldKey = resolveFieldKey(props.rowData, field.field);
            if (!fieldKey || used.has(fieldKey)) {
              return null;
            }
            used.add(fieldKey);
            const abbreviation = consumeMatchingAbbreviation(abbreviationByRoot, abbreviationRootKey(normalizeKey(fieldKey)));
            const value = props.rowData[fieldKey];
            return {
              config: field,
              key: fieldKey,
              value,
              abbreviation,
            };
          })
          .filter(Boolean) as Array<{
          config: ManualFieldConfig;
          key: string;
          value: unknown;
          abbreviation: AbbreviationEntry | null;
        }>;

        if (!resolved.length) {
          return null;
        }

        return (
          <Section key={section.title} title={section.title} className={`details-section ${section.className || ""}`.trim()}>
            <div className="details-section-grid">
              {resolved.map((field) => (
                <label
                  key={field.key}
                  className={`field-item ${resolveSpan(field.config)}`.trim()}
                  style={fieldGridStyle(field.config)}
                >
                  <span className="field-title-row">
                    <span>{field.key}</span>
                    {field.abbreviation && asText(field.abbreviation.value) && <em className="field-abbrev-chip">{asText(field.abbreviation.value)}</em>}
                  </span>
                  <FieldEditor
                    sheet={props.sheet}
                    fieldName={field.key}
                    value={field.value}
                    rowData={props.rowData}
                    validationOptions={resolveValidationOptions(field.key, props.validationCatalog, props.lookupFieldOptions)}
                    validationCatalogByField={props.validationCatalog?.options_by_field || {}}
                    validationCatalogBySheet={props.validationCatalog?.options_by_sheet || {}}
                    onFieldChange={props.onFieldChange}
                    onRowDataPatch={props.onRowDataPatch}
                  />
                </label>
              ))}
            </div>
          </Section>
        );
      })}
    </>
  );
}
