export interface SourceInfo {
  source: string;
  available: boolean;
  reason?: string | null;
}

export interface SpreadsheetSourcesResponse {
  default_source: string;
  sources: SourceInfo[];
}

export interface SpreadsheetSheetsResponse {
  source: string;
  sheets: string[];
}

export interface SpreadsheetRowsResponse {
  source: string;
  sheet: string;
  offset: number;
  limit: number;
  total_rows: number;
  columns: string[];
  rows: Record<string, unknown>[];
}

export interface SpreadsheetRowResponse {
  source: string;
  sheet: string;
  row_number: number;
  header_row: number;
  columns: string[];
  row: Record<string, unknown>;
  sections: RelationSection[];
}

export interface RelationSection {
  section: string;
  sheet: string;
  count: number;
  rows: Record<string, unknown>[];
}

export interface ValidationCatalogResponse {
  source: string;
  sheets: string[];
  options_by_field: Record<string, { field: string; values: string[]; sheet: string }>;
  options_by_sheet: Record<string, Record<string, string[]>>;
}

export interface AppSettingsResponse {
  settings: Record<string, unknown>;
}

export interface MoneyCatalogResponse {
  source: string;
  money_sheet?: string | null;
  matrix_sheet?: string | null;
  currencies: string[];
  matrix: Record<string, Record<string, number>>;
}

export interface TimelineCalendarMonth {
  row_number: number;
  month_order?: string | null;
  month_name?: string | null;
  description?: string | null;
  chore_name?: string | null;
  chore_description?: string | null;
  deity_name?: string | null;
  domain?: string | null;
}

export interface TimelineNamingGroup {
  key: string;
  label: string;
  values: string[];
}

export interface TimelineHoliday {
  row_number?: number | null;
  name: string;
  month_name?: string | null;
  day?: number | null;
  recurrence?: string | null;
  source?: string | null;
  weekday?: string | null;
  year?: string | null;
  notes?: string | null;
}

export interface TimelineEraEvent {
  year?: number | null;
  era?: string | null;
  event: string;
  row_number?: number | null;
  column?: number | null;
}

export interface TimelinePresentDay {
  weekday?: string | null;
  day?: number | null;
  event?: string | null;
}

export interface TimelinePresentWeek {
  week_index?: number | null;
  days: TimelinePresentDay[];
}

export interface TimelinePresentMonth {
  row_start?: number | null;
  column_start?: number | null;
  year_name?: string | null;
  month_name?: string | null;
  weekdays: string[];
  weeks: TimelinePresentWeek[];
  day_count?: number | null;
}

export interface TimelineCatalogResponse {
  source: string;
  calendar_months: TimelineCalendarMonth[];
  naming_groups: TimelineNamingGroup[];
  naming_template?: string | null;
  weekdays: string[];
  holidays: TimelineHoliday[];
  era_events: TimelineEraEvent[];
  present_months: TimelinePresentMonth[];
  summary: Record<string, number>;
}

export interface TranslatorTargetsResponse {
  source: string;
  targets: string[];
}

export interface TranslatorContextResponse {
  source: string;
  target: string;
  dictionary_sheet?: string | null;
  phonetics_sheet?: string | null;
  script_sheet?: string | null;
  grammar_sheet?: string | null;
  sheets: Array<{ sheet: string; rows: Record<string, unknown>[] }>;
}

export interface TranslatorResponse {
  target: string;
  input: string;
  translated: string;
  phonetic?: string | null;
  romanized: string;
  script: string;
  symbolized: string;
  audio_text: string;
  status: string;
  reason?: string | null;
}

export interface FormatterStyleTemplatesResponse {
  templates: Array<{ name: string; label: string }>;
}

export interface FormatterStyleTemplateResponse {
  name: string;
  label: string;
  css: string;
  palette: Array<{ token: string; value: string }>;
}

export interface HealthResponse {
  status: string;
}

export interface LoadingTriviaItem {
  tidbit: string;
  entity_type?: string | null;
  entity_name?: string | null;
  source?: string | null;
}

export interface LoadingTriviaResponse {
  items: LoadingTriviaItem[];
}

export type TabKey =
  | "compendium"
  | "validations"
  | "details"
  | "formatter"
  | "intelligence"
  | "translator"
  | "image"
  | "money"
  | "timeline"
  | "settings";

export interface SelectedRow {
  source: string;
  sheet: string;
  rowNumber: number;
  rowData: Record<string, unknown>;
  sections: RelationSection[];
}
