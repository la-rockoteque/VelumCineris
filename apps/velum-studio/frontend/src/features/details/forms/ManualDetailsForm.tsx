import { useEffect, useState } from "react";
import { styled } from "app/styletron";
import { FieldEditor } from "features/details/FieldEditors";
import type { FieldSuggestionResponse } from "shared/types/api";
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

interface FieldSuggestionState {
  status: "loading" | "ready" | "error";
  response?: FieldSuggestionResponse;
  error?: string;
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

const FieldShell = styled("div", ({ $span }: { $span: ManualFieldConfig["span"] }) => {
  const defaultSpan = 4;
  const computedSpan =
    $span === "full"
      ? "1 / -1"
      : typeof $span === "number" && Number.isFinite($span) && $span > 0
        ? `span ${Math.min(12, Math.max(1, Math.floor($span)))}`
        : `span ${defaultSpan}`;

  return {
    gridColumn: computedSpan,
    position: "relative",
    ":hover [data-field-intelligence='true']": {
      opacity: 1,
      transform: "translateY(0)",
    },
    ":focus-within [data-field-intelligence='true']": {
      opacity: 1,
      transform: "translateY(0)",
    },
    "@media (max-width: 860px)": {
      gridColumn: "span 6",
    },
    "@media (max-width: 560px)": {
      gridColumn: "span 12",
    },
  };
});

const FieldItem = styled("label", {
  display: "flex",
  flexDirection: "column",
  gap: "6px",
  fontSize: "0.82rem",
  color: "var(--ink-soft)",
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

const FieldTitleLeft = styled("span", {
  display: "inline-flex",
  alignItems: "center",
  gap: "8px",
  minWidth: 0,
});

const FieldTitleText = styled("span", {
  display: "inline-flex",
  alignItems: "baseline",
  gap: "6px",
  minWidth: 0,
  flexWrap: "wrap",
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

const FieldSuggestionTrigger = styled("button", {
  width: "22px",
  height: "22px",
  minWidth: "22px",
  padding: 0,
  borderRadius: "999px",
  borderColor: "rgba(82, 107, 133, 0.24)",
  background: "rgba(238, 244, 250, 0.84)",
  color: "#51657d",
  fontSize: "0.8rem",
  lineHeight: 1,
  opacity: 0,
  transform: "translateY(-2px)",
  transition: "opacity 140ms ease, transform 140ms ease, background 140ms ease",
  ":hover": {
    background: "rgba(220, 232, 244, 0.96)",
  },
});

const SuggestionCard = styled("div", {
  display: "grid",
  gap: "8px",
  border: "1px solid rgba(86, 108, 129, 0.22)",
  borderRadius: "10px",
  background: "linear-gradient(180deg, rgba(244, 248, 252, 0.98), rgba(235, 242, 248, 0.96))",
  padding: "10px",
});

const SuggestionMeta = styled("div", {
  display: "flex",
  justifyContent: "space-between",
  alignItems: "center",
  gap: "8px",
  fontSize: "0.68rem",
  fontWeight: 700,
  textTransform: "uppercase",
  letterSpacing: "0.05em",
  color: "#5a6980",
});

const SuggestionStatus = styled("span", {
  fontSize: "0.66rem",
  fontWeight: 800,
  color: "#6e5a2a",
});

const SuggestionValue = styled("div", {
  whiteSpace: "pre-wrap",
  fontSize: "0.82rem",
  lineHeight: 1.5,
  color: "#304252",
});

const SuggestionRationale = styled("div", {
  fontSize: "0.76rem",
  lineHeight: 1.45,
  color: "#526272",
});

const SuggestionActions = styled("div", {
  display: "flex",
  justifyContent: "flex-end",
  gap: "8px",
  flexWrap: "wrap",
});

const SuggestionActionButton = styled("button", {
  border: "1px solid var(--border)",
  borderRadius: "8px",
  background: "var(--surface-strong)",
  color: "var(--ink)",
  fontSize: "0.76rem",
  padding: "6px 10px",
  cursor: "pointer",
});

const SuggestionError = styled("div", {
  fontSize: "0.76rem",
  lineHeight: 1.45,
  color: "#7a3f2f",
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
  suggestionState: FieldSuggestionState | undefined,
  onRequestSuggestion: (fieldName: string, validationOptions: string[]) => void,
  onAcceptSuggestion: (fieldName: string, suggestion: string) => void,
  onDismissSuggestion: (fieldName: string) => void,
) {
  const validationOptions = resolveValidationOptions(
    field.key,
    props.validationCatalog,
    props.lookupFieldOptions,
  );

  return (
    <FieldShell key={field.key} $span={field.config.span}>
      <FieldItem>
        <FieldTitleRow>
          <FieldTitleLeft>
            <FieldSuggestionTrigger
              type="button"
              data-field-intelligence="true"
              title={`Suggest a balanced value for ${field.label}`}
              aria-label={`Suggest balanced value for ${field.label}`}
              onClick={(event) => {
                event.preventDefault();
                event.stopPropagation();
                onRequestSuggestion(field.key, validationOptions);
              }}
            >
              ✦
            </FieldSuggestionTrigger>
            <FieldTitleText>
              <span>{field.label}</span>
              {field.label !== field.key && <FieldKeyHint>{field.key}</FieldKeyHint>}
            </FieldTitleText>
          </FieldTitleLeft>
          {field.abbreviation && asText(field.abbreviation.value) && (
            <AbbrevChip>{asText(field.abbreviation.value)}</AbbrevChip>
          )}
        </FieldTitleRow>
        <FieldEditor
          sheet={props.sheet}
          fieldName={field.key}
          value={field.value}
          rowData={props.rowData}
          validationOptions={validationOptions}
          validationCatalogByField={props.validationCatalog?.options_by_field || {}}
          validationCatalogBySheet={props.validationCatalog?.options_by_sheet || {}}
          onFieldChange={props.onFieldChange}
          onRowDataPatch={props.onRowDataPatch}
        />
      </FieldItem>
      {suggestionState?.status === "loading" && (
        <SuggestionCard>
          <SuggestionMeta>
            <span>Field Intelligence</span>
            <SuggestionStatus>Generating</SuggestionStatus>
          </SuggestionMeta>
          <SuggestionRationale>Consulting ChatGPT with the current item context and balance constraints.</SuggestionRationale>
        </SuggestionCard>
      )}
      {suggestionState?.status === "error" && (
        <SuggestionCard>
          <SuggestionMeta>
            <span>Field Intelligence</span>
            <SuggestionStatus>Error</SuggestionStatus>
          </SuggestionMeta>
          <SuggestionError>{suggestionState.error || "Unable to generate a field suggestion."}</SuggestionError>
          <SuggestionActions>
            <SuggestionActionButton
              type="button"
              aria-label={`Reject suggestion for ${field.label}`}
              onClick={(event) => {
                event.preventDefault();
                event.stopPropagation();
                onDismissSuggestion(field.key);
              }}
            >
              Dismiss
            </SuggestionActionButton>
          </SuggestionActions>
        </SuggestionCard>
      )}
      {suggestionState?.status === "ready" && suggestionState.response && (
        <SuggestionCard>
          <SuggestionMeta>
            <span>{suggestionState.response.provider === "chatgpt" ? "ChatGPT Suggestion" : "Fallback Suggestion"}</span>
            <SuggestionStatus>{suggestionState.response.status}</SuggestionStatus>
          </SuggestionMeta>
          <SuggestionValue>{suggestionState.response.suggested_value || "(No suggested value returned)"}</SuggestionValue>
          <SuggestionRationale>{suggestionState.response.rationale}</SuggestionRationale>
          {suggestionState.response.reason && (
            <SuggestionError>{suggestionState.response.reason}</SuggestionError>
          )}
          <SuggestionActions>
            <SuggestionActionButton
              type="button"
              aria-label={`Reject suggestion for ${field.label}`}
              onClick={(event) => {
                event.preventDefault();
                event.stopPropagation();
                onDismissSuggestion(field.key);
              }}
            >
              Reject
            </SuggestionActionButton>
            <SuggestionActionButton
              type="button"
              aria-label={`Accept suggestion for ${field.label}`}
              onClick={(event) => {
                event.preventDefault();
                event.stopPropagation();
                onAcceptSuggestion(field.key, suggestionState.response?.suggested_value || "");
              }}
            >
              Accept
            </SuggestionActionButton>
          </SuggestionActions>
        </SuggestionCard>
      )}
    </FieldShell>
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
  const [suggestionsByField, setSuggestionsByField] = useState<Record<string, FieldSuggestionState>>({});
  const abbreviationByRoot = buildAbbreviationMap(props.rowData);
  const used = new Set<string>();
  const primaryNameKey = findPrimaryNameFieldKey(props.sheet, props.rowData);
  const rowIdentity = `${props.sheet}:${asText(props.rowData._sheet_row)}`;

  useEffect(() => {
    setSuggestionsByField({});
  }, [rowIdentity]);

  const requestSuggestion = (fieldName: string, validationOptions: string[]) => {
    setSuggestionsByField((current) => ({
      ...current,
      [fieldName]: { status: "loading" },
    }));

    props
      .onSuggestField(fieldName, validationOptions)
      .then((response) => {
        setSuggestionsByField((current) => ({
          ...current,
          [fieldName]: { status: "ready", response },
        }));
      })
      .catch((error: unknown) => {
        setSuggestionsByField((current) => ({
          ...current,
          [fieldName]: {
            status: "error",
            error: error instanceof Error ? error.message : String(error),
          },
        }));
      });
  };

  const acceptSuggestion = (fieldName: string, suggestion: string) => {
    props.onFieldChange(fieldName, suggestion);
    setSuggestionsByField((current) => {
      const next = { ...current };
      delete next[fieldName];
      return next;
    });
  };

  const dismissSuggestion = (fieldName: string) => {
    setSuggestionsByField((current) => {
      const next = { ...current };
      delete next[fieldName];
      return next;
    });
  };

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
                {sectionFields.map((field) =>
                  renderResolvedField(
                    field,
                    props,
                    suggestionsByField[field.key],
                    requestSuggestion,
                    acceptSuggestion,
                    dismissSuggestion,
                  ),
                )}
              </SectionGrid>
            )}

            {subsectionEntries.map((subsection) => (
              <Subsection key={`${section.title}-${subsection.config.title}`}>
                <SubsectionTitle>{subsection.config.title}</SubsectionTitle>
                <SectionGrid>
                  {subsection.fields.map((field) =>
                    renderResolvedField(
                      field,
                      props,
                      suggestionsByField[field.key],
                      requestSuggestion,
                      acceptSuggestion,
                      dismissSuggestion,
                    ),
                  )}
                </SectionGrid>
              </Subsection>
            ))}
          </SectionCard>
        );
      })}
    </>
  );
}
