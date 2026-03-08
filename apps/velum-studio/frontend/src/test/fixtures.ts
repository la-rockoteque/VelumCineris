import type {
  MoneyCatalogResponse,
  SelectedRow,
  TimelineCatalogResponse,
  TranslatorContextResponse,
  ValidationCatalogResponse,
} from "shared/types/api";

export function selectedRow(overrides: Partial<SelectedRow> = {}): SelectedRow {
  return {
    source: "xlsx",
    sheet: "Spells",
    rowNumber: 2,
    rowData: {
      _sheet_row: 2,
      Name: "Arc Flash",
      School: "Evocation",
      Range: "60 feet",
      Description: "A bright arc of energy.",
    },
    sections: [],
    ...overrides,
  };
}

export function validationCatalog(overrides: Partial<ValidationCatalogResponse> = {}): ValidationCatalogResponse {
  return {
    source: "xlsx",
    sheets: ["Spells:Validations"],
    options_by_field: {
      school: { field: "School", values: ["Evocation", "Abjuration"], sheet: "Spells:Validations" },
      class: { field: "Class", values: ["Wizard", "Sorcerer"], sheet: "Spells:Validations" },
    },
    options_by_sheet: {},
    ...overrides,
  };
}

export function moneyCatalog(overrides: Partial<MoneyCatalogResponse> = {}): MoneyCatalogResponse {
  return {
    source: "xlsx",
    money_sheet: "Money",
    matrix_sheet: "Money Matrix",
    currencies: ["gp", "sp"],
    matrix: {
      gp: { sp: 10 },
      sp: { gp: 0.1 },
    },
    ...overrides,
  };
}

export function timelineCatalog(overrides: Partial<TimelineCatalogResponse> = {}): TimelineCatalogResponse {
  return {
    source: "xlsx",
    calendar_months: [{ row_number: 2, month_order: "1", month_name: "Dawn", description: "" }],
    naming_groups: [{ key: "col_1", label: "A (Modifier)", values: ["Radiant"] }],
    naming_template: "Year of the {A (Modifier)}",
    weekdays: ["One", "Two", "Three", "Four", "Five"],
    holidays: [{ name: "First Light", month_name: "Dawn", day: 1, recurrence: "yearly", source: "holidays" }],
    era_events: [{ year: 0, era: "Origins", event: "The world awakens." }],
    present_months: [
      {
        row_start: 1,
        column_start: 1,
        year_name: "Year 0",
        month_name: "Dawn",
        weekdays: ["One", "Two", "Three", "Four", "Five"],
        day_count: 5,
        weeks: [
          {
            week_index: 1,
            days: [
              { weekday: "One", day: 1, event: "First Light" },
              { weekday: "Two", day: 2, event: null },
              { weekday: "Three", day: 3, event: null },
              { weekday: "Four", day: 4, event: null },
              { weekday: "Five", day: 5, event: null },
            ],
          },
        ],
      },
    ],
    summary: { months: 1, naming_groups: 1, weekdays: 5, holidays: 1, era_events: 1, present_months: 1 },
    ...overrides,
  };
}

export function translatorContext(overrides: Partial<TranslatorContextResponse> = {}): TranslatorContextResponse {
  return {
    source: "xlsx",
    target: "Elvish",
    dictionary_sheet: "Elvish:Dictionary",
    phonetics_sheet: "Elvish:Phonetics",
    script_sheet: "Elvish:Script",
    grammar_sheet: "Elvish:Grammar",
    sheets: [
      {
        sheet: "Elvish:Dictionary",
        rows: [{ English: "Light", Elvish: "Lumen" }],
      },
    ],
    ...overrides,
  };
}
