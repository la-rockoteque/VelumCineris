import { useMemo } from "react";
import { styled } from "app/styletron";

import { syncLinkedSpellFields, syncSpellComponentAbbreviation, useEditableTitle } from "features/details/FieldEditors";
import {
  BackgroundDetailsForm,
  FeatDetailsForm,
  GenericDetailsForm,
  MonsterDetailsForm,
  SpeciesDetailsForm,
  SpellDetailsForm,
} from "features/details/forms";
import type { ItemDetailsFormProps } from "features/details/forms/types";
import { Button, Card, EditableTitle, MetaText } from "shared/library";
import type { SelectedRow, ValidationCatalogResponse } from "shared/types/api";
import {
  findRowKeyByNormalized,
  groupDetailFields,
  isBackgroundSheet,
  isFeatSheet,
  isMonsterSheet,
  isSpeciesSheet,
  isSpellSheet,
  stripNameFields,
} from "shared/utils/fields";
import { isRemoteImage, resolveRowImage } from "shared/utils/image";
import { asText, normalizeKey, truncateText } from "shared/utils/text";

interface DetailsTabProps {
  loading: boolean;
  selected: SelectedRow | null;
  validationCatalog: ValidationCatalogResponse | null;
  cellCharLimit: number;
  actionMode: "dry_run" | "live";
  onActionModeChange: (mode: "dry_run" | "live") => void;
  onRowDataChange: (next: Record<string, unknown>) => void;
  onItemAction: (integrationKey: string, operation: string, dryRun: boolean) => Promise<void>;
  lookupFieldOptions: (fieldName: string) => string[];
}

const DetailsWorkspace = styled("div", {
  gap: "12px",
});

const DetailsShell = styled("div", {
  marginTop: "6px",
  display: "grid",
  gap: "14px",
  gridTemplateColumns: "minmax(280px, 360px) minmax(0, 1fr)",
  alignItems: "start",
  "@media (max-width: 1100px)": {
    gridTemplateColumns: "1fr",
  },
});

const DetailsSidebar = styled("aside", {
  display: "grid",
  gap: "10px",
  alignContent: "start",
  position: "sticky",
  top: "12px",
  "@media (max-width: 1100px)": {
    position: "static",
  },
});

const SidebarPanel = styled("section", {
  border: "1px solid var(--border)",
  borderRadius: "12px",
  padding: "12px",
  background: "var(--surface-strong)",
});

const SidebarPanelTitle = styled("h4", {
  margin: "0 0 8px",
  fontSize: "0.85rem",
  textTransform: "uppercase",
  letterSpacing: "0.04em",
  color: "var(--ink-soft)",
});

const IntegrationActions = styled("div", {
  display: "grid",
  gap: "8px",
  gridTemplateColumns: "repeat(auto-fit, minmax(130px, 1fr))",
  marginTop: "10px",
});

const FullWidthButton = styled("button", {
  border: "1px solid var(--border)",
  borderRadius: "9px",
  padding: "8px 10px",
  font: "inherit",
  color: "var(--ink)",
  background: "var(--surface-strong)",
  cursor: "pointer",
  fontWeight: 600,
  width: "100%",
  ":disabled": {
    opacity: 0.6,
    cursor: "not-allowed",
  },
  ":hover:not(:disabled)": {
    borderColor: "rgba(155, 77, 31, 0.5)",
  },
});

const Main = styled("main", {
  display: "grid",
  gap: "12px",
  alignContent: "start",
  width: "100%",
  maxInlineSize: "min(1320px, calc(100vw - 440px))",
  "@media (max-width: 1100px)": {
    maxInlineSize: "100%",
  },
});

const Hero = styled("section", {
  border: "1px solid var(--border)",
  borderRadius: "12px",
  padding: "12px",
  background: "#f8efdf",
  display: "grid",
  gap: "12px",
  gridTemplateColumns: "minmax(0, 1fr) 260px",
  alignItems: "start",
  "@media (max-width: 1100px)": {
    gridTemplateColumns: "1fr",
  },
});

const HeroInfo = styled("div", {
  display: "grid",
  gap: "8px",
});

const HeroSubtitle = styled("p", {
  margin: 0,
  color: "var(--ink-soft)",
  fontSize: "0.86rem",
});

const HeroStatus = styled("div", {
  display: "flex",
  flexWrap: "wrap",
  gap: "6px",
});

const StatusChip = styled("span", {
  border: "1px solid rgba(66, 48, 30, 0.16)",
  borderRadius: "999px",
  padding: "3px 8px",
  fontSize: "0.68rem",
  color: "#6d624f",
  background: "rgba(255, 249, 238, 0.78)",
});

const HeroChips = styled("div", {
  display: "flex",
  flexWrap: "wrap",
  gap: "8px",
});

const Chip = styled("span", {
  border: "1px solid var(--border)",
  borderRadius: "999px",
  padding: "4px 10px",
  fontSize: "0.74rem",
  color: "#5d513f",
  background: "rgba(255, 250, 240, 0.9)",
});

const Media = styled("div", {
  border: "1px solid rgba(66, 48, 30, 0.24)",
  borderRadius: "10px",
  overflow: "hidden",
  background: "#efe2cf",
  minHeight: "220px",
  display: "grid",
  gridTemplateRows: "minmax(0, 1fr) auto",
});

const MediaImage = styled("img", {
  width: "100%",
  height: "100%",
  minHeight: "180px",
  objectFit: "cover",
  display: "block",
});

const MediaMeta = styled("div", {
  display: "flex",
  justifyContent: "space-between",
  gap: "8px",
  alignItems: "center",
  padding: "8px 10px",
  background: "rgba(255, 249, 238, 0.95)",
  fontSize: "0.72rem",
  color: "#635744",
});

const MediaMetaLink = styled("a", {
  color: "var(--accent)",
  textDecoration: "none",
  fontWeight: 700,
  ":hover": {
    textDecoration: "underline",
  },
});

const MediaFallback = styled("div", {
  minHeight: "220px",
  display: "grid",
  placeItems: "center",
  textAlign: "center",
  fontSize: "0.85rem",
  letterSpacing: "0.02em",
  color: "#6b604f",
  padding: "12px",
});

const RelationSection = styled("section", {
  border: "1px solid var(--border)",
  borderRadius: "12px",
  padding: "12px",
  background: "#f7f0e5",
});

const RelationTitle = styled("h3", {
  margin: 0,
  fontSize: "0.9rem",
  textTransform: "uppercase",
  letterSpacing: "0.04em",
});

const RelationTableWrap = styled("div", {
  marginTop: "10px",
  border: "1px solid var(--border)",
  borderRadius: "14px",
  overflow: "auto",
  maxHeight: "60vh",
  background: "var(--surface-strong)",
});

function isHeaderStatusField(normalized: string): boolean {
  return (
    (normalized.includes("ddb") || normalized.includes("worldanvil") || normalized.includes("obsidian") || normalized.includes("sync")) &&
    !normalized.includes("id")
  );
}

function buildStatusChips(rowData: Record<string, unknown>): string[] {
  const out: string[] = [];
  for (const [key, value] of Object.entries(rowData)) {
    const text = asText(value);
    if (!text) {
      continue;
    }
    if (!isHeaderStatusField(normalizeKey(key))) {
      continue;
    }
    out.push(`${key}: ${truncateText(text, 32)}`);
  }
  return out.slice(0, 8);
}

function buildMetaChips(rowData: Record<string, unknown>): string[] {
  const keys = ["Type", "Subtype", "Class", "Level", "School", "CR", "Source", "Alignment", "Size"];
  const out: string[] = [];
  for (const label of keys) {
    const key = findRowKeyByNormalized(rowData, [label]);
    if (!key) {
      continue;
    }
    const text = asText(rowData[key]);
    if (!text) {
      continue;
    }
    out.push(`${label}: ${text}`);
    if (out.length >= 5) {
      break;
    }
  }
  return out;
}

function chooseDetailsForm(props: ItemDetailsFormProps) {
  if (isSpellSheet(props.sheet)) {
    return <SpellDetailsForm {...props} />;
  }
  if (isMonsterSheet(props.sheet)) {
    return <MonsterDetailsForm {...props} />;
  }
  if (isSpeciesSheet(props.sheet)) {
    return <SpeciesDetailsForm {...props} />;
  }
  if (isBackgroundSheet(props.sheet)) {
    return <BackgroundDetailsForm {...props} />;
  }
  if (isFeatSheet(props.sheet)) {
    return <FeatDetailsForm {...props} />;
  }
  return <GenericDetailsForm {...props} />;
}

export function DetailsTab(props: DetailsTabProps) {
  const selected = props.selected;
  const titleBinding = useEditableTitle(selected?.sheet || "", selected?.rowData || {});

  const grouped = useMemo(() => {
    if (!selected) {
      return null;
    }
    const groupedFields = groupDetailFields(selected.sheet, selected.rowData);
    return stripNameFields(selected.sheet, selected.rowData, groupedFields);
  }, [selected]);

  const statusChips = useMemo(() => (selected ? buildStatusChips(selected.rowData) : []), [selected]);
  const metaChips = useMemo(() => (selected ? buildMetaChips(selected.rowData) : []), [selected]);
  const image = useMemo(() => (selected ? resolveRowImage(selected.rowData) : null), [selected]);

  const changeField = (fieldName: string, value: unknown) => {
    if (!selected) {
      return;
    }
    const patch = syncLinkedSpellFields(selected.sheet, fieldName, selected.rowData, value);
    const mergedPatch = syncSpellComponentAbbreviation(selected.rowData, patch);
    props.onRowDataChange({ ...selected.rowData, ...mergedPatch });
  };

  const setTitle = (nextTitle: string) => {
    if (!selected || !titleBinding.titleKey) {
      return;
    }
    props.onRowDataChange({ ...selected.rowData, [titleBinding.titleKey]: nextTitle });
  };

  if (!selected || !grouped) {
    return (
      <Card title="Details Editor" subtitle="Select a row from Compendium to view contextual details and actions.">
        <></>
      </Card>
    );
  }

  const formProps: ItemDetailsFormProps = {
    sheet: selected.sheet,
    grouped,
    rowData: selected.rowData,
    validationCatalog: props.validationCatalog,
    lookupFieldOptions: props.lookupFieldOptions,
    onFieldChange: changeField,
    onRowDataPatch: (patch) => props.onRowDataChange({ ...selected.rowData, ...patch }),
  };

  return (
    <Card title="Details Editor" subtitle={`${selected.sheet} | row ${selected.rowNumber}`}>
      <DetailsWorkspace>
        <DetailsShell>
          <DetailsSidebar>
            <SidebarPanel>
              <SidebarPanelTitle>Actions</SidebarPanelTitle>
              <label>
                Mode
                <select
                  value={props.actionMode}
                  onChange={(event) => props.onActionModeChange(event.target.value === "live" ? "live" : "dry_run")}
                  disabled={props.loading}
                >
                  <option value="dry_run">Dry Run</option>
                  <option value="live">Live Execute</option>
                </select>
              </label>
              <IntegrationActions>
                <FullWidthButton disabled={props.loading} onClick={() => void props.onItemAction("worldanvil", "publish", props.actionMode !== "live")}>
                  WA Publish
                </FullWidthButton>
                <FullWidthButton disabled={props.loading} onClick={() => void props.onItemAction("worldanvil", "delete", props.actionMode !== "live")}>
                  WA Delete
                </FullWidthButton>
                <FullWidthButton disabled={props.loading} onClick={() => void props.onItemAction("dndbeyond", "publish", props.actionMode !== "live")}>
                  DDB Publish
                </FullWidthButton>
                <FullWidthButton disabled={props.loading} onClick={() => void props.onItemAction("dndbeyond", "delete", props.actionMode !== "live")}>
                  DDB Delete
                </FullWidthButton>
                <FullWidthButton disabled={props.loading} onClick={() => void props.onItemAction("obsidianportal", "publish", props.actionMode !== "live")}>
                  OP Publish
                </FullWidthButton>
                <FullWidthButton disabled={props.loading} onClick={() => void props.onItemAction("obsidianportal", "delete", props.actionMode !== "live")}>
                  OP Delete
                </FullWidthButton>
              </IntegrationActions>
            </SidebarPanel>

            {!!selected.sections.length && (
              <SidebarPanel>
                <SidebarPanelTitle>Related</SidebarPanelTitle>
                <MetaText>{selected.sections.reduce((acc, section) => acc + Number(section.count || 0), 0)} linked rows</MetaText>
              </SidebarPanel>
            )}
          </DetailsSidebar>

          <Main>
            <Hero>
              <HeroInfo>
                <EditableTitle value={titleBinding.title} placeholder="Selected Item" editable={Boolean(titleBinding.titleKey)} onCommit={setTitle} />

                <HeroSubtitle>
                  {selected.sheet} row {selected.rowNumber}
                </HeroSubtitle>

                {!!statusChips.length && (
                  <HeroStatus>
                    {statusChips.map((chip) => (
                      <StatusChip key={chip}>{chip}</StatusChip>
                    ))}
                  </HeroStatus>
                )}

                {!!metaChips.length && (
                  <HeroChips>
                    {metaChips.map((chip) => (
                      <Chip key={chip}>{chip}</Chip>
                    ))}
                  </HeroChips>
                )}
              </HeroInfo>

              <Media>
                {image ? (
                  <>
                    <MediaImage src={image.url} alt={`${titleBinding.title || "item"} illustration`} loading="lazy" />
                    <MediaMeta>
                      <span>Source field: {image.field}</span>
                      {isRemoteImage(image.url) && (
                        <MediaMetaLink href={image.url} target="_blank" rel="noopener noreferrer">
                          Open image
                        </MediaMetaLink>
                      )}
                    </MediaMeta>
                  </>
                ) : (
                  <MediaFallback>No image mapped</MediaFallback>
                )}
              </Media>
            </Hero>

            {chooseDetailsForm(formProps)}

            {!!selected.sections.length &&
              selected.sections
                .filter((section) => section.rows && section.rows.length)
                .map((section) => {
                  const columns = Object.keys(section.rows[0] || {});
                  return (
                    <RelationSection key={`${section.section}-${section.sheet}`}>
                      <RelationTitle>{`${section.section} (${section.count})`}</RelationTitle>
                      <RelationTableWrap>
                        <table>
                          <thead>
                            <tr>
                              {columns.map((column) => (
                                <th key={column}>{column}</th>
                              ))}
                            </tr>
                          </thead>
                          <tbody>
                            {section.rows.map((row, index) => (
                              <tr key={`${section.sheet}-${index}`}>
                                {columns.map((column) => {
                                  const full = asText(row[column]);
                                  const short = truncateText(full, props.cellCharLimit);
                                  return (
                                    <td key={`${index}-${column}`} title={short !== full ? full : undefined}>
                                      {short}
                                    </td>
                                  );
                                })}
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </RelationTableWrap>
                    </RelationSection>
                  );
                })}
          </Main>
        </DetailsShell>
      </DetailsWorkspace>
    </Card>
  );
}
