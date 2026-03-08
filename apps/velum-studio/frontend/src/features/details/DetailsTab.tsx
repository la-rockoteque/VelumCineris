import { useMemo } from "react";

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
import { Card, EditableTitle, Section, Subsection } from "shared/library";
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
    <Card title="Details Editor" subtitle={`${selected.sheet} | row ${selected.rowNumber}`} className="details-workspace">
      <>
        <div className="details-shell">
          <aside className="details-sidebar">
            <Subsection title="Actions" className="workspace-card">
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
              <div className="integration-actions" style={{ marginTop: 10 }}>
                <button className="btn" disabled={props.loading} onClick={() => void props.onItemAction("worldanvil", "publish", props.actionMode !== "live")}>WA Publish</button>
                <button className="btn" disabled={props.loading} onClick={() => void props.onItemAction("worldanvil", "delete", props.actionMode !== "live")}>WA Delete</button>
                <button className="btn" disabled={props.loading} onClick={() => void props.onItemAction("dndbeyond", "publish", props.actionMode !== "live")}>DDB Publish</button>
                <button className="btn" disabled={props.loading} onClick={() => void props.onItemAction("dndbeyond", "delete", props.actionMode !== "live")}>DDB Delete</button>
                <button className="btn" disabled={props.loading} onClick={() => void props.onItemAction("obsidianportal", "publish", props.actionMode !== "live")}>OP Publish</button>
                <button className="btn" disabled={props.loading} onClick={() => void props.onItemAction("obsidianportal", "delete", props.actionMode !== "live")}>OP Delete</button>
              </div>
            </Subsection>

            {!!selected.sections.length && (
              <Subsection title="Related" className="workspace-card">
                <div className="meta">{selected.sections.reduce((acc, section) => acc + Number(section.count || 0), 0)} linked rows</div>
              </Subsection>
            )}
          </aside>

          <main className="details-main">
            <section className="details-hero">
              <div className="details-hero-info">
                <EditableTitle
                  className={titleBinding.titleKey ? "details-title-editable" : ""}
                  value={titleBinding.title}
                  placeholder="Selected Item"
                  editable={Boolean(titleBinding.titleKey)}
                  onCommit={setTitle}
                />

                <p className="details-hero-subtitle">
                  {selected.sheet} row {selected.rowNumber}
                </p>

                {!!statusChips.length && (
                  <div className="details-hero-status">
                    {statusChips.map((chip) => (
                      <span key={chip} className="details-status-chip">
                        {chip}
                      </span>
                    ))}
                  </div>
                )}

                {!!metaChips.length && (
                  <div className="details-hero-chips">
                    {metaChips.map((chip) => (
                      <span key={chip} className="details-chip">
                        {chip}
                      </span>
                    ))}
                  </div>
                )}
              </div>

              <div className="details-media">
                {image ? (
                  <>
                    <img src={image.url} alt={`${titleBinding.title || "item"} illustration`} loading="lazy" />
                    <div className="details-media-meta">
                      <span>Source field: {image.field}</span>
                      {isRemoteImage(image.url) && (
                        <a href={image.url} target="_blank" rel="noopener noreferrer">
                          Open image
                        </a>
                      )}
                    </div>
                  </>
                ) : (
                  <div className="details-media-fallback">No image mapped</div>
                )}
              </div>
            </section>

            {chooseDetailsForm(formProps)}

            {!!selected.sections.length &&
              selected.sections
                .filter((section) => section.rows && section.rows.length)
                .map((section) => {
                  const columns = Object.keys(section.rows[0] || {});
                  return (
                    <Section key={`${section.section}-${section.sheet}`} className="relation-section" title={`${section.section} (${section.count})`}>
                      <div className="table-wrap">
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
                      </div>
                    </Section>
                  );
                })}
          </main>
        </div>
      </>
    </Card>
  );
}
