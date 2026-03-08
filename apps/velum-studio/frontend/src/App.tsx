import { useEffect, useMemo, useRef, useState } from "react";

import { CurrentItemProvider, CurrentSheetProvider, useCurrentItem, useCurrentSheet } from "app/currentSelectionContext";
import { useAppData } from "app/useAppData";
import { useToasts } from "app/useToasts";
import { ErrorBanner } from "components/ErrorBanner";
import { LoadingOverlay } from "components/LoadingOverlay";
import { ToastHost } from "components/ToastHost";
import { CompendiumTab } from "features/compendium/CompendiumTab";
import { DetailsTab } from "features/details/DetailsTab";
import { FormatterTab } from "features/formatter/FormatterTab";
import { ImageTab } from "features/image/ImageTab";
import { IntelligenceTab } from "features/intelligence/IntelligenceTab";
import { MoneyTab } from "features/money/MoneyTab";
import { SettingsTab } from "features/settings/SettingsTab";
import { TimelineTab } from "features/timeline/TimelineTab";
import { TranslatorTab } from "features/translator/TranslatorTab";
import { ValidationsTab } from "features/validations/ValidationsTab";
import type { HealthResponse, TabKey } from "shared/types/api";

const tabs: Array<{ key: TabKey; label: string }> = [
  { key: "compendium", label: "Compendium" },
  { key: "validations", label: "Validations" },
  { key: "details", label: "Details Editor" },
  { key: "formatter", label: "Formatters" },
  { key: "intelligence", label: "Intelligence" },
  { key: "translator", label: "Translator" },
  { key: "image", label: "Image Generator" },
  { key: "money", label: "Money" },
  { key: "timeline", label: "Timeline" },
  { key: "settings", label: "Settings" },
];

function HeaderSelectionStatus(props: { health: "ok" | "warn" }) {
  const sheet = useCurrentSheet();
  const item = useCurrentItem();

  const sheetLabel = sheet.sheet ? `${sheet.sheet} (${sheet.source})` : `No sheet (${sheet.source})`;
  const itemLabel = item.selected ? `${item.name || "Unnamed"} · #${item.selected.rowNumber}` : "No item selected";

  return (
    <div className="app-header-status">
      <div className={`pill ${props.health === "ok" ? "ok" : "warn"}`}>{props.health === "ok" ? "API healthy" : "API unavailable"}</div>
      <div className="app-selection-pills">
        <div className="pill info">Sheet: {sheetLabel}</div>
        <div className="pill info">Item: {itemLabel}</div>
      </div>
    </div>
  );
}

export default function App() {
  const { state, actions } = useAppData();
  const toasts = useToasts();
  const [health, setHealth] = useState<"ok" | "warn">("warn");
  const [itemActionMode, setItemActionMode] = useState<"dry_run" | "live">("dry_run");
  const lastErrorRef = useRef("");

  useEffect(() => {
    void (async () => {
      try {
        const response = await fetch("/health");
        const payload = (await response.json()) as HealthResponse;
        setHealth(payload.status === "ok" ? "ok" : "warn");
      } catch {
        setHealth("warn");
      }
    })();
  }, []);

  useEffect(() => {
    if (!state.error || state.error === lastErrorRef.current) {
      return;
    }
    lastErrorRef.current = state.error;
    toasts.push(state.error, "error");
  }, [state.error, toasts]);

  const cellCharLimit = useMemo(() => {
    const compendium = (state.settings.compendium as Record<string, unknown> | undefined) || {};
    return Number(compendium.cell_char_limit ?? 150);
  }, [state.settings]);

  const currentSheet = useMemo(
    () => ({
      source: state.source,
      sheet: state.sheet,
    }),
    [state.sheet, state.source],
  );

  const onOpenContext = async (rowNumber: number, tab: "details" | "intelligence" | "image") => {
    const payload = await actions.selectRow(rowNumber, tab);
    if (payload) {
      toasts.push(`Selected row #${rowNumber}.`, "info");
    }
  };

  const onIntegrationAction = async (rowNumber: number, integration: string, operation: string) => {
    await actions.selectRow(rowNumber, state.activeTab);
    const response = await actions.runItemIntegrationAction(integration, operation, itemActionMode !== "live");
    if (!response) {
      return;
    }
    const status = String((response as { status?: string }).status || "ok");
    if (status.toLowerCase().includes("error") || status.toLowerCase().includes("failed")) {
      toasts.push(`${integration} ${operation} failed.`, "error");
    } else {
      toasts.push(`${integration} ${operation} completed (${itemActionMode === "live" ? "live" : "dry-run"}).`, "success");
    }
  };

  return (
    <>
      <div className="bg-shape bg-a" />
      <div className="bg-shape bg-b" />

      <CurrentSheetProvider value={currentSheet}>
        <CurrentItemProvider value={state.selected}>
          <main className="app-shell">
            <header className="app-header">
              <div>
                <h1>Velum Studio</h1>
                <p>Spreadsheet-first desktop workflow for compendium authoring and publishing.</p>
              </div>
              <HeaderSelectionStatus health={health} />
            </header>

            <ErrorBanner error={state.error} onClose={actions.clearError} />

            <nav className="tabs" aria-label="Workspace tabs">
              {tabs.map((tab) => (
                <button
                  key={tab.key}
                  type="button"
                  className={`tab ${state.activeTab === tab.key ? "active" : ""}`.trim()}
                  onClick={() => actions.setActiveTab(tab.key)}
                >
                  {tab.label}
                </button>
              ))}
            </nav>

            {state.activeTab === "compendium" && (
              <section className="panel active">
                <CompendiumTab
                  loading={state.loading}
                  sources={state.sources}
                  source={state.source}
                  sheets={state.sheets}
                  sheet={state.sheet}
                  query={state.query}
                  limit={state.limit}
                  offset={state.offset}
                  totalRows={state.totalRows}
                  columns={state.columns}
                  visibleColumns={state.visibleColumns}
                  rows={state.rows}
                  cellCharLimit={cellCharLimit}
                  onSourceChange={async (value) => {
                    await actions.setSource(value);
                  }}
                  onSheetChange={async (value) => {
                    await actions.setSheet(value);
                  }}
                  onQueryChange={(value) => actions.setQuery(value)}
                  onRunSearch={async () => {
                    await actions.runSearch();
                  }}
                  onLimitChange={async (value) => {
                    await actions.setLimit(value);
                  }}
                  onPrevPage={async () => {
                    await actions.prevPage();
                  }}
                  onNextPage={async () => {
                    await actions.nextPage();
                  }}
                  onRefresh={async () => {
                    await actions.refreshRows();
                  }}
                  onVisibleColumnsChange={async (columns) => {
                    await actions.setVisibleColumns(columns);
                  }}
                  onOpenContext={onOpenContext}
                  onIntegrationAction={onIntegrationAction}
                />
              </section>
            )}

        {state.activeTab === "validations" && (
          <section className="panel active">
            <ValidationsTab
              loading={state.loading}
              source={state.source}
              validationSheets={state.validationSheets}
              cellCharLimit={cellCharLimit}
              onLoadValidationRows={(sheet) => actions.loadValidationSheetRows(sheet)}
            />
          </section>
        )}

        {state.activeTab === "details" && (
          <section className="panel active">
            <DetailsTab
              loading={state.loading}
              selected={state.selected}
              validationCatalog={state.validationCatalog}
              cellCharLimit={cellCharLimit}
              actionMode={itemActionMode}
              onActionModeChange={setItemActionMode}
              onRowDataChange={(next) => actions.setSelectedRowData(next)}
              onItemAction={(integrationKey, operation, dryRun) =>
                actions
                  .runItemIntegrationAction(integrationKey, operation, dryRun)
                  .then((response) => {
                    if (!response) {
                      return;
                    }
                    toasts.push(`${integrationKey} ${operation} completed (${dryRun ? "dry-run" : "live"}).`, "success");
                  })
              }
              lookupFieldOptions={actions.lookupFieldOptions}
            />
          </section>
        )}

        {state.activeTab === "formatter" && (
          <section className="panel active">
            <FormatterTab
              loading={state.loading}
              source={state.source}
              sheets={state.sheets}
              selected={state.selected}
              settings={state.settings}
              output={state.formatterOutput}
              onSelectRow={async (rowNumber, sheet) => {
                if (sheet !== state.sheet) {
                  await actions.setSheet(sheet);
                }
                await actions.selectRow(rowNumber, "formatter");
              }}
              onLoadRows={(sheet) => actions.loadValidationSheetRows(sheet)}
              onRunPreview={(payload) =>
                actions.callFormatterPreview(payload).then((response) => {
                  if (!response) {
                    return null;
                  }
                  actions.saveFormatterOutput(JSON.stringify(response, null, 2));
                  toasts.push("Formatter preview generated.", "success");
                  return response;
                })
              }
              onLoadTemplates={() => actions.loadFormatterStyles().then((payload) => (payload as { templates?: Array<{ name: string; label: string }> } | null))}
              onLoadTemplate={(name) =>
                actions
                  .loadFormatterStyleTemplate(name)
                  .then((payload) => (payload as { css?: string; palette?: Array<{ token: string; value: string }> } | null))
              }
              onSaveSettingsPatch={(patch) =>
                actions.saveSettingsPatch(patch).then(() => {
                  toasts.push("Formatter style settings saved.", "success");
                })
              }
            />
          </section>
        )}

        {state.activeTab === "intelligence" && (
          <section className="panel active">
            <IntelligenceTab
              loading={state.loading}
              selected={state.selected}
              output={state.intelligenceOutput}
              onRun={(payload) =>
                actions.runIntelligence(payload).then((response) => {
                  if (response) {
                    toasts.push("Intelligence suggestions ready.", "success");
                  }
                  return response;
                })
              }
            />
          </section>
        )}

        {state.activeTab === "translator" && (
          <section className="panel active">
            <TranslatorTab
              loading={state.loading}
              source={state.source}
              selected={state.selected}
              output={state.translatorOutput}
              romanized={state.translatorRomanized}
              symbolized={state.translatorSymbolized}
              context={state.translatorContext}
              onLoadTargets={() => actions.loadTranslatorTargets()}
              onLoadContext={(target) => actions.loadTranslatorContext(target)}
              onTranslate={(target, text) =>
                actions.translate(target, text).then(() => {
                  toasts.push("Translation complete.", "success");
                })
              }
            />
          </section>
        )}

        {state.activeTab === "image" && (
          <section className="panel active">
            <ImageTab
              loading={state.loading}
              selected={state.selected}
              output={state.imageOutput}
              onRun={(payload) =>
                actions.runImagePlan(payload).then((response) => {
                  if (response) {
                    toasts.push("Image generation plan ready.", "success");
                  }
                  return response;
                })
              }
            />
          </section>
        )}

        {state.activeTab === "money" && (
          <section className="panel active">
            <MoneyTab
              loading={state.loading}
              moneyCatalog={state.moneyCatalog}
              onRefresh={() =>
                actions.loadMoneyCatalog().then(() => {
                  toasts.push("Money catalog refreshed.", "success");
                })
              }
            />
          </section>
        )}

        {state.activeTab === "timeline" && (
          <section className="panel active">
            <TimelineTab
              loading={state.loading}
              timelineCatalog={state.timelineCatalog}
              onReload={() =>
                actions.loadTimelineCatalog().then(() => {
                  toasts.push("Timeline reloaded.", "success");
                })
              }
              onSaveCatalog={(payload) =>
                actions.saveTimelineCatalog(payload).then(() => {
                  toasts.push("Timeline saved.", "success");
                })
              }
            />
          </section>
        )}

            {state.activeTab === "settings" && (
              <section className="panel active">
                <SettingsTab
                  loading={state.loading}
                  source={state.source}
                  settings={state.settings}
                  onSavePatch={(patch) =>
                    actions.saveSettingsPatch(patch).then(() => {
                      toasts.push("Settings saved.", "success");
                    })
                  }
                  onResetColumns={() =>
                    actions.resetCurrentSheetColumns().then(() => {
                      toasts.push("Column visibility reset for current sheet.", "success");
                    })
                  }
                />
              </section>
            )}
          </main>

          <LoadingOverlay visible={state.loading} message="Working" />
          <ToastHost items={toasts.items} onDismiss={toasts.dismiss} />
        </CurrentItemProvider>
      </CurrentSheetProvider>
    </>
  );
}
