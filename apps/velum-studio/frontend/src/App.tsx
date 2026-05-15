import { useEffect, useMemo, useRef, useState } from "react";
import { brickAndMossUrl } from "@velum/dsm";
import { styled } from "app/styletron";

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
import { Badge, TabBar } from "shared/library";
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

const riseInAnimation = {
  from: {
    opacity: 0,
    transform: "translateY(14px)",
  },
  to: {
    opacity: 1,
    transform: "translateY(0)",
  },
};

const fadeInAnimation = {
  from: {
    opacity: 0,
    transform: "translateY(8px)",
  },
  to: {
    opacity: 1,
    transform: "translateY(0)",
  },
};

const AppRoot = styled("div", {
  minHeight: "100vh",
  color: "var(--ink)",
  background: `url("${brickAndMossUrl}") center / cover fixed no-repeat`,
  overflowX: "hidden",
});

const BgShapeA = styled("div", {
  position: "fixed",
  borderRadius: "999px",
  filter: "blur(44px)",
  pointerEvents: "none",
  opacity: 0.45,
  width: "380px",
  height: "380px",
  top: "-80px",
  right: "-120px",
  background: "#c99863",
});

const BgShapeB = styled("div", {
  position: "fixed",
  borderRadius: "999px",
  filter: "blur(44px)",
  pointerEvents: "none",
  opacity: 0.45,
  width: "300px",
  height: "300px",
  bottom: "-120px",
  left: "-90px",
  background: "#7d9566",
});

const AppShell = styled("main", {
  maxWidth: "1440px",
  margin: "28px auto",
  padding: "20px",
  border: "1px solid var(--border)",
  borderRadius: "20px",
  background: "var(--surface)",
  backdropFilter: "blur(8px)",
  animationName: riseInAnimation,
  animationDuration: "320ms",
  animationTimingFunction: "ease-out",
  "@media (max-width: 860px)": {
    margin: "12px",
    padding: "14px",
    borderRadius: "14px",
  },
});

const AppHeader = styled("header", {
  display: "flex",
  justifyContent: "space-between",
  alignItems: "flex-start",
  gap: "16px",
  "@media (max-width: 860px)": {
    flexDirection: "column",
    alignItems: "stretch",
  },
});

const AppTitle = styled("h1", {
  margin: 0,
  fontFamily: "\"Avenir Next Condensed\", \"Franklin Gothic Medium\", sans-serif",
  letterSpacing: "0.05em",
  textTransform: "uppercase",
});

const AppSubtitle = styled("p", {
  margin: "6px 0 0",
  color: "var(--ink-soft)",
});

const HeaderStatus = styled("div", {
  display: "grid",
  gap: "8px",
  justifyItems: "end",
  "@media (max-width: 860px)": {
    justifyItems: "start",
  },
});

const SelectionPills = styled("div", {
  display: "flex",
  flexWrap: "wrap",
  gap: "8px",
  justifyContent: "flex-end",
  "@media (max-width: 860px)": {
    justifyContent: "flex-start",
  },
});

const Tabs = styled("div", {
  marginTop: "20px",
});

const Panel = styled("section", {
  marginTop: "16px",
  display: "block",
  animationName: fadeInAnimation,
  animationDuration: "240ms",
  animationTimingFunction: "ease",
});

function HeaderSelectionStatus(props: { health: "ok" | "warn" }) {
  const sheet = useCurrentSheet();
  const item = useCurrentItem();

  const sheetLabel = sheet.sheet ? `${sheet.sheet} (${sheet.source})` : `No sheet (${sheet.source})`;
  const itemLabel = item.selected ? `${item.name || "Unnamed"} · #${item.selected.rowNumber}` : "No item selected";

  return (
    <HeaderStatus>
      <Badge tone={props.health === "ok" ? "ok" : "warn"}>{props.health === "ok" ? "API healthy" : "API unavailable"}</Badge>
      <SelectionPills>
        <Badge tone="info">Sheet: {sheetLabel}</Badge>
        <Badge tone="info">Item: {itemLabel}</Badge>
      </SelectionPills>
    </HeaderStatus>
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
    <AppRoot>
      <BgShapeA />
      <BgShapeB />

      <CurrentSheetProvider value={currentSheet}>
        <CurrentItemProvider value={state.selected}>
          <AppShell>
            <AppHeader>
              <div>
                <AppTitle>Velum Studio</AppTitle>
                <AppSubtitle>Spreadsheet-first desktop workflow for compendium authoring and publishing.</AppSubtitle>
              </div>
              <HeaderSelectionStatus health={health} />
            </AppHeader>

            <ErrorBanner error={state.error} onClose={actions.clearError} />

            <Tabs>
              <TabBar
                ariaLabel="Workspace tabs"
                activeKey={state.activeTab}
                onChange={(value) => actions.setActiveTab(value as TabKey)}
                layout="wrap"
                size="sm"
                items={tabs.map((tab) => ({
                  key: tab.key,
                  label: tab.label,
                }))}
              />
            </Tabs>

            {state.activeTab === "compendium" && (
              <Panel>
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
              </Panel>
            )}

        {state.activeTab === "validations" && (
          <Panel>
            <ValidationsTab
              loading={state.loading}
              source={state.source}
              validationSheets={state.validationSheets}
              cellCharLimit={cellCharLimit}
              onLoadValidationRows={(sheet) => actions.loadValidationSheetRows(sheet)}
            />
          </Panel>
        )}

        {state.activeTab === "details" && (
          <Panel>
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
              onSuggestField={(fieldName, validationOptions) => actions.requestFieldSuggestion(fieldName, validationOptions)}
            />
          </Panel>
        )}

        {state.activeTab === "formatter" && (
          <Panel>
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
          </Panel>
        )}

        {state.activeTab === "intelligence" && (
          <Panel>
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
          </Panel>
        )}

        {state.activeTab === "translator" && (
          <Panel>
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
          </Panel>
        )}

        {state.activeTab === "image" && (
          <Panel>
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
          </Panel>
        )}

        {state.activeTab === "money" && (
          <Panel>
            <MoneyTab
              loading={state.loading}
              moneyCatalog={state.moneyCatalog}
              onRefresh={() =>
                actions.loadMoneyCatalog().then(() => {
                  toasts.push("Money catalog refreshed.", "success");
                })
              }
            />
          </Panel>
        )}

        {state.activeTab === "timeline" && (
          <Panel>
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
          </Panel>
        )}

            {state.activeTab === "settings" && (
              <Panel>
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
              </Panel>
            )}
          </AppShell>

          <LoadingOverlay visible={state.loading} message="Working" />
          <ToastHost items={toasts.items} onDismiss={toasts.dismiss} />
        </CurrentItemProvider>
      </CurrentSheetProvider>
    </AppRoot>
  );
}
