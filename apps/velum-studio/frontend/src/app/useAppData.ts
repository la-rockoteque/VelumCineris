import { useQueryClient } from "@tanstack/react-query";
import { useCallback, useEffect, useMemo, useState } from "react";

import { apiDelete, apiGet, apiPost, apiPut } from "shared/api/client";
import type {
  AppSettingsResponse,
  MoneyCatalogResponse,
  SelectedRow,
  SourceInfo,
  SpreadsheetRowResponse,
  SpreadsheetRowsResponse,
  SpreadsheetSheetsResponse,
  SpreadsheetSourcesResponse,
  TabKey,
  TimelineCatalogResponse,
  TranslatorContextResponse,
  TranslatorResponse,
  ValidationCatalogResponse,
} from "shared/types/api";
import { normalizeKey } from "shared/utils/text";

export interface AppDataState {
  loading: boolean;
  error: string;
  activeTab: TabKey;
  source: string;
  sources: SourceInfo[];
  sheet: string;
  sheets: string[];
  validationSheets: string[];
  validationCatalog: ValidationCatalogResponse | null;
  settings: Record<string, unknown>;
  rows: Record<string, unknown>[];
  columns: string[];
  visibleColumns: string[];
  totalRows: number;
  offset: number;
  limit: number;
  query: string;
  selected: SelectedRow | null;
  moneyCatalog: MoneyCatalogResponse | null;
  timelineCatalog: TimelineCatalogResponse | null;
  formatterOutput: string;
  intelligenceOutput: string;
  imageOutput: string;
  translatorOutput: string;
  translatorContext: TranslatorContextResponse | null;
  translatorRomanized: string;
  translatorSymbolized: string;
}

function getStoredVisibleColumns(settings: Record<string, unknown>, source: string, sheet: string): string[] {
  const key = `${source.toLowerCase()}::${sheet}`;
  const columns = (settings.sheet_columns as Record<string, { visible_columns?: string[] }> | undefined)?.[key]?.visible_columns;
  return Array.isArray(columns) ? columns : [];
}

function selectDefaultVisibleColumns(
  allColumns: string[],
  settings: Record<string, unknown>,
  source: string,
  sheet: string,
): string[] {
  const saved = getStoredVisibleColumns(settings, source, sheet);
  if (saved.length) {
    return saved.filter((column) => allColumns.includes(column));
  }
  const compendium = (settings.compendium as Record<string, unknown> | undefined) ?? {};
  const minimalEnabled = Boolean(compendium.minimal_columns_default ?? true);
  const minimalCount = Number(compendium.minimal_column_count ?? 8);
  if (!minimalEnabled) {
    return allColumns;
  }
  return allColumns.slice(0, Math.max(1, minimalCount));
}

const queryKeys = {
  settings: ["settings"] as const,
  sources: ["sources"] as const,
  compendiumSheets: (source: string) => ["compendium-sheets", source] as const,
  validationSheets: (source: string) => ["validation-sheets", source] as const,
  validationCatalog: (source: string) => ["validation-catalog", source] as const,
  rows: (source: string, sheet: string, offset: number, limit: number, query: string) =>
    ["rows", source, sheet, offset, limit, query] as const,
  rowsPrefix: (source: string, sheet: string) => ["rows", source, sheet] as const,
  row: (source: string, sheet: string, rowNumber: number) => ["row", source, sheet, rowNumber] as const,
  moneyCatalog: (source: string) => ["money-catalog", source] as const,
  timelineCatalog: (source: string) => ["timeline-catalog", source] as const,
  translatorTargets: (source: string) => ["translator-targets", source] as const,
  translatorContext: (source: string, target: string) => ["translator-context", source, target] as const,
  formatterStyles: ["formatter-styles"] as const,
  formatterStyleTemplate: (name: string) => ["formatter-style-template", name] as const,
};

export function useAppData() {
  const queryClient = useQueryClient();

  const [state, setState] = useState<AppDataState>({
    loading: false,
    error: "",
    activeTab: "compendium",
    source: "auto",
    sources: [],
    sheet: "",
    sheets: [],
    validationSheets: [],
    validationCatalog: null,
    settings: {},
    rows: [],
    columns: [],
    visibleColumns: [],
    totalRows: 0,
    offset: 0,
    limit: 50,
    query: "",
    selected: null,
    moneyCatalog: null,
    timelineCatalog: null,
    formatterOutput: "Run a formatter preview from a selected row.",
    intelligenceOutput: "Suggestions will appear here.",
    imageOutput: "Image generation plan appears here.",
    translatorOutput: "Translation result appears here.",
    translatorContext: null,
    translatorRomanized: "",
    translatorSymbolized: "",
  });

  const withLoading = useCallback(async <T,>(task: () => Promise<T>): Promise<T | null> => {
    setState((current) => ({ ...current, loading: true, error: "" }));
    try {
      const result = await task();
      setState((current) => ({ ...current, loading: false }));
      return result;
    } catch (err) {
      setState((current) => ({
        ...current,
        loading: false,
        error: err instanceof Error ? err.message : String(err),
      }));
      return null;
    }
  }, []);

  const loadSettings = useCallback(async () => {
    const payload = await queryClient.fetchQuery({
      queryKey: queryKeys.settings,
      queryFn: () => apiGet<AppSettingsResponse>("/api/settings"),
    });
    setState((current) => ({ ...current, settings: payload.settings ?? {} }));
    return payload.settings ?? {};
  }, [queryClient]);

  const loadSources = useCallback(async () => {
    const payload = await queryClient.fetchQuery({
      queryKey: queryKeys.sources,
      queryFn: () => apiGet<SpreadsheetSourcesResponse>("/api/spreadsheet/sources"),
    });

    setState((current) => ({
      ...current,
      sources: payload.sources ?? [],
      source: current.source === "auto" ? payload.default_source || current.source : current.source,
    }));

    return payload;
  }, [queryClient]);

  const loadSheets = useCallback(
    async (source: string) => {
      const [sheetPayload, validationPayload] = await Promise.all([
        queryClient.fetchQuery({
          queryKey: queryKeys.compendiumSheets(source),
          queryFn: () => apiGet<SpreadsheetSheetsResponse>(`/api/compendium/sheets?source=${encodeURIComponent(source)}`),
        }),
        queryClient.fetchQuery({
          queryKey: queryKeys.validationSheets(source),
          queryFn: () => apiGet<SpreadsheetSheetsResponse>(`/api/validations/sheets?source=${encodeURIComponent(source)}`),
        }),
      ]);

      setState((current) => {
        const nextSheet = sheetPayload.sheets.includes(current.sheet) ? current.sheet : sheetPayload.sheets[0] || "";
        return {
          ...current,
          source,
          sheets: sheetPayload.sheets,
          validationSheets: validationPayload.sheets,
          sheet: nextSheet,
          offset: 0,
        };
      });

      return {
        sheets: sheetPayload.sheets,
        validationSheets: validationPayload.sheets,
      };
    },
    [queryClient],
  );

  const loadValidationCatalog = useCallback(
    async (source: string) => {
      const payload = await queryClient.fetchQuery({
        queryKey: queryKeys.validationCatalog(source),
        queryFn: () => apiGet<ValidationCatalogResponse>(`/api/validations/catalog?source=${encodeURIComponent(source)}`),
      });
      setState((current) => ({ ...current, validationCatalog: payload }));
      return payload;
    },
    [queryClient],
  );

  const loadRows = useCallback(
    async (params?: { source?: string; sheet?: string; offset?: number; limit?: number; query?: string }) => {
      const source = params?.source ?? state.source;
      const sheet = params?.sheet ?? state.sheet;
      const offset = params?.offset ?? state.offset;
      const limit = params?.limit ?? state.limit;
      const query = params?.query ?? state.query;

      if (!sheet) {
        return null;
      }

      const payload = await queryClient.fetchQuery({
        queryKey: queryKeys.rows(source, sheet, offset, limit, query),
        queryFn: () =>
          apiGet<SpreadsheetRowsResponse>(
            `/api/spreadsheet/rows?source=${encodeURIComponent(source)}&sheet=${encodeURIComponent(sheet)}&offset=${offset}&limit=${limit}&q=${encodeURIComponent(query)}`,
          ),
      });

      setState((current) => ({
        ...current,
        source: payload.source,
        sheet: payload.sheet,
        rows: payload.rows,
        columns: payload.columns,
        totalRows: payload.total_rows,
        offset,
        limit,
        query,
        visibleColumns: selectDefaultVisibleColumns(payload.columns, current.settings, payload.source, payload.sheet),
      }));

      return payload;
    },
    [queryClient, state.limit, state.offset, state.query, state.sheet, state.source],
  );

  const selectRow = useCallback(
    async (rowNumber: number, activateTab: TabKey = "details") => {
      const payload = await queryClient.fetchQuery({
        queryKey: queryKeys.row(state.source, state.sheet, rowNumber),
        queryFn: () =>
          apiGet<SpreadsheetRowResponse>(
            `/api/spreadsheet/row?source=${encodeURIComponent(state.source)}&sheet=${encodeURIComponent(state.sheet)}&row_number=${rowNumber}`,
          ),
      });

      setState((current) => ({
        ...current,
        selected: {
          source: payload.source,
          sheet: payload.sheet,
          rowNumber: payload.row_number,
          rowData: payload.row,
          sections: payload.sections ?? [],
        },
        activeTab: activateTab,
      }));

      return payload;
    },
    [queryClient, state.sheet, state.source],
  );

  const saveVisibleColumns = useCallback(
    async (columns: string[]) => {
      if (!state.sheet) {
        return;
      }
      await apiPut<AppSettingsResponse, { source: string; sheet: string; visible_columns: string[] }>("/api/settings/columns", {
        source: state.source,
        sheet: state.sheet,
        visible_columns: columns,
      });

      await queryClient.invalidateQueries({ queryKey: queryKeys.settings });
      setState((current) => ({ ...current, visibleColumns: columns }));
    },
    [queryClient, state.sheet, state.source],
  );

  const resetCurrentSheetColumns = useCallback(async () => {
    if (!state.sheet) {
      return;
    }

    const payload = await apiDelete<AppSettingsResponse>(
      `/api/settings/columns?source=${encodeURIComponent(state.source)}&sheet=${encodeURIComponent(state.sheet)}`,
    );

    await queryClient.invalidateQueries({ queryKey: queryKeys.settings });
    await queryClient.invalidateQueries({ queryKey: queryKeys.rowsPrefix(state.source, state.sheet) });

    setState((current) => ({ ...current, settings: payload.settings ?? current.settings }));
    await loadRows();
  }, [loadRows, queryClient, state.sheet, state.source]);

  const saveSettingsPatch = useCallback(
    async (patch: Record<string, unknown>) => {
      const payload = await apiPut<AppSettingsResponse, { patch: Record<string, unknown> }>("/api/settings", { patch });
      await queryClient.invalidateQueries({ queryKey: queryKeys.settings });
      await queryClient.invalidateQueries({ queryKey: queryKeys.sources });
      setState((current) => ({ ...current, settings: payload.settings ?? current.settings }));
      return payload;
    },
    [queryClient],
  );

  const loadMoneyCatalog = useCallback(async () => {
    const payload = await queryClient.fetchQuery({
      queryKey: queryKeys.moneyCatalog(state.source),
      queryFn: () => apiGet<MoneyCatalogResponse>(`/api/money/catalog?source=${encodeURIComponent(state.source)}`),
    });
    setState((current) => ({ ...current, moneyCatalog: payload }));
    return payload;
  }, [queryClient, state.source]);

  const loadTimelineCatalog = useCallback(async () => {
    const payload = await queryClient.fetchQuery({
      queryKey: queryKeys.timelineCatalog(state.source),
      queryFn: () => apiGet<TimelineCatalogResponse>(`/api/timeline/catalog?source=${encodeURIComponent(state.source)}`),
    });
    setState((current) => ({ ...current, timelineCatalog: payload }));
    return payload;
  }, [queryClient, state.source]);

  const saveTimelineCatalog = useCallback(
    async (payload: Record<string, unknown>) => {
      const next = await apiPut<TimelineCatalogResponse, Record<string, unknown>>("/api/timeline/catalog", {
        source: state.source,
        ...payload,
      });
      queryClient.setQueryData(queryKeys.timelineCatalog(state.source), next);
      setState((current) => ({ ...current, timelineCatalog: next }));
      return next;
    },
    [queryClient, state.source],
  );

  const loadTranslatorContext = useCallback(
    async (target: string) => {
      const payload = await queryClient.fetchQuery({
        queryKey: queryKeys.translatorContext(state.source, target),
        queryFn: () =>
          apiGet<TranslatorContextResponse>(
            `/api/translator/context?source=${encodeURIComponent(state.source)}&target=${encodeURIComponent(target)}`,
          ),
      });
      setState((current) => ({ ...current, translatorContext: payload }));
      return payload;
    },
    [queryClient, state.source],
  );

  const translate = useCallback(
    async (target: string, text: string) => {
      const payload = await apiPost<TranslatorResponse, { source: string; target: string; text: string }>("/api/translator/translate", {
        source: state.source,
        target,
        text,
      });

      setState((current) => ({
        ...current,
        translatorOutput: JSON.stringify(payload, null, 2),
        translatorRomanized: payload.romanized || payload.audio_text || "",
        translatorSymbolized: payload.symbolized || payload.script || "",
      }));
      return payload;
    },
    [state.source],
  );

  const lookupFieldOptions = useCallback(
    (fieldName: string): string[] => {
      const catalog = state.validationCatalog?.options_by_field ?? {};
      const normalized = normalizeKey(fieldName);
      const direct = catalog[normalized]?.values;
      if (Array.isArray(direct)) {
        return direct;
      }
      return [];
    },
    [state.validationCatalog],
  );

  useEffect(() => {
    void withLoading(async () => {
      const settings = await loadSettings();
      const sources = await loadSources();
      const preferred = typeof settings?.default_source === "string" ? settings.default_source : "";
      const availableSources = (sources?.sources || []).filter((item) => item.available).map((item) => item.source);
      const source = preferred && availableSources.includes(preferred) ? preferred : sources?.default_source || state.source;
      await loadSheets(source);
      await loadValidationCatalog(source);
      await loadRows({ source });
      await loadMoneyCatalog();
      await loadTimelineCatalog();
      setState((current) => ({
        ...current,
        settings: settings ?? current.settings,
      }));
    });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const actions = useMemo(
    () => ({
      setActiveTab: (tab: TabKey) => setState((current) => ({ ...current, activeTab: tab })),
      setSource: async (source: string) =>
        withLoading(async () => {
          await loadSheets(source);
          await loadValidationCatalog(source);
          await loadRows({ source, offset: 0 });
          await loadMoneyCatalog();
          await loadTimelineCatalog();
        }),
      setSheet: async (sheet: string) =>
        withLoading(async () => {
          setState((current) => ({ ...current, sheet, offset: 0 }));
          await loadRows({ sheet, offset: 0 });
        }),
      setLimit: async (limit: number) =>
        withLoading(async () => {
          setState((current) => ({ ...current, limit, offset: 0 }));
          await loadRows({ limit, offset: 0 });
        }),
      setQuery: (query: string) => setState((current) => ({ ...current, query })),
      runSearch: async () => withLoading(async () => loadRows({ offset: 0 })),
      nextPage: async () =>
        withLoading(async () => {
          const nextOffset = state.offset + state.limit;
          if (nextOffset >= state.totalRows) {
            return;
          }
          await loadRows({ offset: nextOffset });
        }),
      prevPage: async () =>
        withLoading(async () => {
          const prevOffset = Math.max(0, state.offset - state.limit);
          await loadRows({ offset: prevOffset });
        }),
      refreshRows: async () => withLoading(async () => loadRows()),
      selectRow: async (rowNumber: number, tab: TabKey = "details") => withLoading(async () => selectRow(rowNumber, tab)),
      setVisibleColumns: async (columns: string[]) => withLoading(async () => saveVisibleColumns(columns)),
      resetCurrentSheetColumns: async () => withLoading(async () => resetCurrentSheetColumns()),
      saveSettingsPatch: async (patch: Record<string, unknown>) => withLoading(async () => saveSettingsPatch(patch)),
      loadValidationSheetRows: async (sheet: string) =>
        withLoading(async () =>
          queryClient.fetchQuery({
            queryKey: queryKeys.rows(state.source, sheet, 0, 500, ""),
            queryFn: () =>
              apiGet<SpreadsheetRowsResponse>(
                `/api/spreadsheet/rows?source=${encodeURIComponent(state.source)}&sheet=${encodeURIComponent(sheet)}&offset=0&limit=500&q=`,
              ),
          }),
        ),
      loadMoneyCatalog: async () => withLoading(async () => loadMoneyCatalog()),
      loadTimelineCatalog: async () => withLoading(async () => loadTimelineCatalog()),
      saveTimelineCatalog: async (payload: Record<string, unknown>) => withLoading(async () => saveTimelineCatalog(payload)),
      loadTranslatorTargets: async () =>
        withLoading(async () =>
          queryClient.fetchQuery({
            queryKey: queryKeys.translatorTargets(state.source),
            queryFn: () => apiGet<{ source: string; targets: string[] }>(`/api/translator/targets?source=${encodeURIComponent(state.source)}`),
          }),
        ),
      loadTranslatorContext: async (target: string) => withLoading(async () => loadTranslatorContext(target)),
      translate: async (target: string, text: string) => withLoading(async () => translate(target, text)),
      callFormatterPreview: async (body: Record<string, unknown>) =>
        withLoading(async () => apiPost<Record<string, unknown>, Record<string, unknown>>("/api/book-formatter/preview", body)),
      loadFormatterStyles: async () =>
        withLoading(async () =>
          queryClient.fetchQuery({
            queryKey: queryKeys.formatterStyles,
            queryFn: () => apiGet<Record<string, unknown>>("/api/formatter/styles"),
          }),
        ),
      loadFormatterStyleTemplate: async (name: string) =>
        withLoading(async () =>
          queryClient.fetchQuery({
            queryKey: queryKeys.formatterStyleTemplate(name),
            queryFn: () => apiGet<Record<string, unknown>>(`/api/formatter/styles/template?name=${encodeURIComponent(name)}`),
          }),
        ),
      saveFormatterOutput: (text: string) => setState((current) => ({ ...current, formatterOutput: text })),
      runItemIntegrationAction: async (integrationKey: string, operation = "publish", dryRun = true) =>
        withLoading(async () => {
          if (!state.selected) {
            throw new Error("Select a row first");
          }
          return apiPost<Record<string, unknown>, Record<string, unknown>>(`/api/items/${encodeURIComponent(integrationKey)}/action`, {
            source: state.selected.source,
            sheet: state.selected.sheet,
            row_number: state.selected.rowNumber,
            operation,
            dry_run: dryRun,
          });
        }),
      runIntelligence: async (body: Record<string, unknown>) =>
        withLoading(async () => {
          const payload = await apiPost<Record<string, unknown>, Record<string, unknown>>("/api/intelligence/suggest", body);
          setState((current) => ({ ...current, intelligenceOutput: JSON.stringify(payload, null, 2) }));
          return payload;
        }),
      runImagePlan: async (body: Record<string, unknown>) =>
        withLoading(async () => {
          const payload = await apiPost<Record<string, unknown>, Record<string, unknown>>("/api/image-generator/generate", body);
          setState((current) => ({ ...current, imageOutput: JSON.stringify(payload, null, 2) }));
          return payload;
        }),
      setSelectedRowData: (next: Record<string, unknown>) =>
        setState((current) => ({
          ...current,
          selected: current.selected
            ? {
                ...current.selected,
                rowData: next,
              }
            : null,
        })),
      clearError: () => setState((current) => ({ ...current, error: "" })),
      lookupFieldOptions,
    }),
    [
      loadMoneyCatalog,
      loadRows,
      loadSheets,
      loadTimelineCatalog,
      loadTranslatorContext,
      loadValidationCatalog,
      lookupFieldOptions,
      queryClient,
      resetCurrentSheetColumns,
      saveSettingsPatch,
      saveTimelineCatalog,
      saveVisibleColumns,
      selectRow,
      state.limit,
      state.offset,
      state.query,
      state.selected,
      state.source,
      state.totalRows,
      translate,
      withLoading,
    ],
  );

  return {
    state,
    actions,
  };
}
