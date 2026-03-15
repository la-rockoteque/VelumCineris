import { styled } from "app/styletron";
import { FieldEditor } from "features/details/FieldEditors";
import { findPrimaryNameFieldKey, findRowKeyByNormalized } from "shared/utils/fields";
import { asText, normalizeKey } from "shared/utils/text";

import type {
  ItemDetailsFormProps,
  ManualFieldConfig,
  ManualSectionConfig,
  ManualSubsectionConfig,
} from "./types";

interface AbbreviationEntry {
  key: string;
  normalized: string;
  value: unknown;
}

interface ResolvedField {
  config: ManualFieldConfig;
  key: string;
  label: string;
  value: unknown;
  abbreviation: AbbreviationEntry | null;
}

function isAbbreviationField(normalizedField: string): boolean {
  return ["abbreviation", "abbr", "abrv", "abvr"].some((token) =>
    normalizedField.includes(token),
  );
}

function abbreviationRootKey(normalizedField: string): string {
  return normalizedField.replace(/abbreviation|abbr|abrv|abvr/g, "");
}

function consumeMatchingAbbreviation(
  map: Map<string, AbbreviationEntry>,
  fieldRoot: string,
): AbbreviationEntry | null {
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

function fieldCandidates(config: ManualFieldConfig): string[] {
  const primary = Array.isArray(config.field) ? config.field : [config.field];
  return [...primary, ...(config.aliases || [])].filter(Boolean);
}

function resolveFieldKey(
  rowData: Record<string, unknown>,
  config: ManualFieldConfig,
): string {
  const candidates = fieldCandidates(config);
  if (!candidates.length) {
    return "";
  }
  return findRowKeyByNormalized(rowData, candidates);
}

const SectionCard = styled("section", ({ $isDescription }: { $isDescription: boolean }) => ({
  border: "1px solid var(--border)",
  borderRadius: "12px",
  padding: "12px",
  background: "#fbf4e7",
  ...($isDescription
    ? {
        textarea: {
          minHeight: "300px",
        },
      }
    : {}),
}));

const SectionTitle = styled("h3", {
  margin: 0,
  fontSize: "0.88rem",
  textTransform: "uppercase",
  letterSpacing: "0.04em",
  color: "var(--ink-soft)",
});

const Subsection = styled("div", {
  marginTop: "12px",
  paddingTop: "10px",
  borderTop: "1px dashed rgba(74, 56, 39, 0.22)",
});

const SubsectionTitle = styled("h4", {
  margin: "0 0 8px",
  fontSize: "0.76rem",
  textTransform: "uppercase",
  letterSpacing: "0.05em",
  color: "#6d624f",
});

const SectionGrid = styled("div", {
  marginTop: "10px",
  display: "grid",
  gridTemplateColumns: "repeat(12, minmax(0, 1fr))",
  gap: "10px",
});

const FieldItem = styled("label", ({ $span }: { $span: ManualFieldConfig["span"] }) => {
  const defaultSpan = 4;
  const computedSpan =
    $span === "full"
      ? "1 / -1"
      : typeof $span === "number" && Number.isFinite($span) && $span > 0
        ? `span ${Math.min(12, Math.max(1, Math.floor($span)))}`
        : `span ${defaultSpan}`;

  return {
    gridColumn: computedSpan,
    display: "flex",
    flexDirection: "column",
    gap: "6px",
    fontSize: "0.82rem",
    color: "var(--ink-soft)",
    "@media (max-width: 860px)": {
      gridColumn: "span 6",
    },
    "@media (max-width: 560px)": {
      gridColumn: "span 12",
    },
  };
});

const FieldTitleRow = styled("span", {
  display: "flex",
  alignItems: "center",
  justifyContent: "space-between",
  gap: "8px",
  fontSize: "0.74rem",
  fontWeight: 700,
  textTransform: "uppercase",
  letterSpacing: "0.03em",
  color: "#645a49",
});

const FieldTitleText = styled("span", {
  display: "inline-flex",
  alignItems: "baseline",
  gap: "6px",
});

const FieldKeyHint = styled("small", {
  fontSize: "0.64rem",
  textTransform: "none",
  letterSpacing: "0.01em",
  color: "#857862",
});

const AbbrevChip = styled("em", {
  fontStyle: "normal",
  fontSize: "0.66rem",
  fontWeight: 700,
  textTransform: "none",
  color: "#756a56",
  border: "1px solid rgba(66, 48, 30, 0.16)",
  borderRadius: "999px",
  padding: "2px 8px",
  background: "rgba(250, 242, 231, 0.92)",
});

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

function resolveConfiguredFields(
  configs: ManualFieldConfig[],
  rowData: Record<string, unknown>,
  used: Set<string>,
  abbreviationByRoot: Map<string, AbbreviationEntry>,
): ResolvedField[] {
  return configs
    .map((config) => {
      const fieldKey = resolveFieldKey(rowData, config);
      if (!fieldKey || used.has(fieldKey)) {
        return null;
      }

      used.add(fieldKey);
      const abbreviation = consumeMatchingAbbreviation(
        abbreviationByRoot,
        abbreviationRootKey(normalizeKey(fieldKey)),
      );

      return {
        config,
        key: fieldKey,
        label: config.label || fieldKey,
        value: rowData[fieldKey],
        abbreviation,
      };
    })
    .filter(Boolean) as ResolvedField[];
}

function renderResolvedField(
  field: ResolvedField,
  props: ItemDetailsFormProps,
) {
  return (
    <FieldItem key={field.key} $span={field.config.span}>
      <FieldTitleRow>
        <FieldTitleText>
          <span>{field.label}</span>
          {field.label !== field.key && <FieldKeyHint>{field.key}</FieldKeyHint>}
        </FieldTitleText>
        {field.abbreviation && asText(field.abbreviation.value) && (
          <AbbrevChip>{asText(field.abbreviation.value)}</AbbrevChip>
        )}
      </FieldTitleRow>
      <FieldEditor
        sheet={props.sheet}
        fieldName={field.key}
        value={field.value}
        rowData={props.rowData}
        validationOptions={resolveValidationOptions(
          field.key,
          props.validationCatalog,
          props.lookupFieldOptions,
        )}
        validationCatalogByField={props.validationCatalog?.options_by_field || {}}
        validationCatalogBySheet={props.validationCatalog?.options_by_sheet || {}}
        onFieldChange={props.onFieldChange}
        onRowDataPatch={props.onRowDataPatch}
      />
    </FieldItem>
  );
}

function resolveRemainingFieldConfigs(
  rowData: Record<string, unknown>,
  used: Set<string>,
  primaryNameKey: string,
): ManualFieldConfig[] {
  const remaining: ManualFieldConfig[] = [];

  for (const key of Object.keys(rowData)) {
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
    remaining.push({ field: key });
  }

  return remaining;
}

function resolveSectionSubsections(
  section: ManualSectionConfig,
  rowData: Record<string, unknown>,
  used: Set<string>,
  abbreviationByRoot: Map<string, AbbreviationEntry>,
): Array<{ config: ManualSubsectionConfig; fields: ResolvedField[] }> {
  return (section.subsections || [])
    .map((subsection) => ({
      config: subsection,
      fields: resolveConfiguredFields(
        subsection.fields,
        rowData,
        used,
        abbreviationByRoot,
      ),
    }))
    .filter((entry) => entry.fields.length > 0);
}

export function ManualDetailsForm(
  props: ItemDetailsFormProps & { schema: ManualSectionConfig[] },
) {
  const abbreviationByRoot = buildAbbreviationMap(props.rowData);
  const used = new Set<string>();
  const primaryNameKey = findPrimaryNameFieldKey(props.sheet, props.rowData);

  return (
    <>
      {props.schema.map((section) => {
        const sectionFields = resolveConfiguredFields(
          section.fields || [],
          props.rowData,
          used,
          abbreviationByRoot,
        );
        const subsectionEntries = resolveSectionSubsections(
          section,
          props.rowData,
          used,
          abbreviationByRoot,
        );

        if (section.includeRemaining) {
          sectionFields.push(
            ...resolveConfiguredFields(
              resolveRemainingFieldConfigs(props.rowData, used, primaryNameKey),
              props.rowData,
              used,
              abbreviationByRoot,
            ),
          );
        }

        if (!sectionFields.length && !subsectionEntries.length) {
          return null;
        }

        const isDescription =
          section.className?.includes("details-section--description") ?? false;

        return (
          <SectionCard key={section.title} $isDescription={isDescription}>
            <SectionTitle>{section.title}</SectionTitle>

            {!!sectionFields.length && (
              <SectionGrid>
                {sectionFields.map((field) => renderResolvedField(field, props))}
              </SectionGrid>
            )}

            {subsectionEntries.map((subsection) => (
              <Subsection key={`${section.title}-${subsection.config.title}`}>
                <SubsectionTitle>{subsection.config.title}</SubsectionTitle>
                <SectionGrid>
                  {subsection.fields.map((field) => renderResolvedField(field, props))}
                </SectionGrid>
              </Subsection>
            ))}
          </SectionCard>
        );
      })}
    </>
  );
}
