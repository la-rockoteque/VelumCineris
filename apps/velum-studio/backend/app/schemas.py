from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class SourceInfo(BaseModel):
    source: str
    available: bool
    reason: str | None = None


class SpreadsheetSourcesResponse(BaseModel):
    default_source: str
    sources: list[SourceInfo]


class SpreadsheetSheetsResponse(BaseModel):
    source: str
    sheets: list[str]


class SpreadsheetSheetSchemaResponse(BaseModel):
    source: str
    sheet: str
    header_row: int
    is_validation_sheet: bool
    columns: list[str]
    validation_columns: list[str]


class SpreadsheetRowsResponse(BaseModel):
    source: str
    sheet: str
    offset: int
    limit: int
    total_rows: int
    columns: list[str]
    rows: list[dict[str, Any]]


class LoadingTriviaItem(BaseModel):
    tidbit: str
    entity_type: str | None = None
    entity_name: str | None = None
    source: str | None = None


class LoadingTriviaResponse(BaseModel):
    items: list[LoadingTriviaItem] = Field(default_factory=list)


class SpreadsheetRowResponse(BaseModel):
    source: str
    sheet: str
    row_number: int
    header_row: int
    columns: list[str]
    row: dict[str, Any]
    sections: list[dict[str, Any]] = Field(default_factory=list)


class IntegrationCard(BaseModel):
    key: str
    label: str
    status: str = Field(description="planned | connected | disabled")
    description: str
    missing_env: list[str] = Field(default_factory=list)
    target_sheets: list[str] = Field(default_factory=list)


class IntegrationListResponse(BaseModel):
    integrations: list[IntegrationCard]


class IntegrationIdentity(BaseModel):
    key: str
    label: str
    description: str


class IntegrationStatusResponse(BaseModel):
    key: str
    label: str
    description: str
    status: str
    source: str
    required_env: list[str]
    missing_env: list[str]
    target_sheets: list[str]
    resolved_target_sheets: list[str]
    missing_target_sheets: list[str]


class IntegrationSheetPreview(BaseModel):
    sheet: str
    name_column: str | None = None
    id_columns: list[str]
    total_rows: int
    truncated: bool = False
    already_synced: int
    sync_candidates: int
    sample_names: list[str]


class IntegrationTotals(BaseModel):
    sheets: int
    rows: int
    sync_candidates: int


class IntegrationPreviewRequest(BaseModel):
    source: str = "auto"
    limit_per_sheet: int = Field(default=1000, ge=1, le=100000)
    include_samples: int = Field(default=3, ge=0, le=20)


class IntegrationPreviewResponse(BaseModel):
    integration: IntegrationIdentity
    source: str
    status: str
    missing_env: list[str]
    sheet_preview: list[IntegrationSheetPreview]
    totals: IntegrationTotals


class IntegrationSyncRequest(BaseModel):
    source: str = "auto"
    dry_run: bool = True
    limit_per_sheet: int = Field(default=1000, ge=1, le=100000)
    include_samples: int = Field(default=3, ge=0, le=20)


class IntegrationPlannedOperation(BaseModel):
    sheet: str
    action: str
    estimated_operations: int
    estimated_skips: int


class IntegrationSyncResponse(BaseModel):
    integration: IntegrationIdentity
    source: str
    dry_run: bool
    planned_operations: list[IntegrationPlannedOperation]
    totals: IntegrationTotals
    message: str


class ItemActionRequest(BaseModel):
    source: str = "auto"
    sheet: str
    row_number: int = Field(ge=1)
    operation: str | None = Field(default="publish")
    dry_run: bool = True


class ItemActionResponse(BaseModel):
    integration_key: str
    integration_label: str | None = None
    status: str
    sheet_supported: bool
    sheet: str
    row_number: int
    name: str
    existing_external_id: str | None = None
    existing_id_column: str | None = None
    operation: str | None = None
    requested_operation: str | None = None
    dry_run: bool
    reason: str
    missing_env: list[str]
    execution_detail: dict[str, Any] | None = None


class BookFormatterRequest(BaseModel):
    source: str = "auto"
    sheet: str
    row_number: int = Field(ge=1)
    targets: list[str] = Field(default_factory=lambda: ["homebrewery"])
    style_template: str | None = None
    style_css: str | None = None


class BookFormatterTargetResult(BaseModel):
    target: str
    status: str
    artifact_type: str | None = None
    artifact_preview: str | None = None
    document_title: str | None = None
    dry_run_steps: list[str] | None = None


class BookFormatterResponse(BaseModel):
    sheet: str
    row_number: int
    title: str
    targets: list[BookFormatterTargetResult]
    summary: str


class FormatterStyleTemplateInfo(BaseModel):
    name: str
    label: str


class FormatterStyleTemplatesResponse(BaseModel):
    templates: list[FormatterStyleTemplateInfo] = Field(default_factory=list)


class FormatterStyleToken(BaseModel):
    token: str
    value: str


class FormatterStyleTemplateResponse(BaseModel):
    name: str
    label: str
    css: str
    palette: list[FormatterStyleToken] = Field(default_factory=list)


class IntelligenceRequest(BaseModel):
    mode: str = "custom"
    instruction: str = ""
    row_data: dict[str, Any] | None = None
    use_local_llm: bool = True
    model: str = "llama3.1:8b"


class IntelligenceResponse(BaseModel):
    mode: str
    provider: str
    model: str
    status: str
    reason: str | None = None
    suggestions: str


class FieldSuggestionRequest(BaseModel):
    sheet: str
    field_name: str
    row_data: dict[str, Any] | None = None
    validation_options: list[str] = Field(default_factory=list)
    model: str = "gpt-5-mini"


class FieldSuggestionResponse(BaseModel):
    provider: str
    model: str
    status: str
    field_name: str
    current_value: str = ""
    suggested_value: str = ""
    rationale: str = ""
    reason: str | None = None


class TranslatorTargetsResponse(BaseModel):
    source: str
    targets: list[str]


class TranslatorRequest(BaseModel):
    source: str = "auto"
    target: str
    text: str


class TranslatorResponse(BaseModel):
    target: str
    sheet: str | None = None
    input: str
    translated: str
    phonetic: str | None = None
    romanized: str
    script: str
    symbolized: str
    audio_text: str
    status: str
    reason: str | None = None


class TranslatorContextSheet(BaseModel):
    sheet: str
    rows: list[dict[str, Any]] = Field(default_factory=list)


class TranslatorContextResponse(BaseModel):
    source: str
    target: str
    dictionary_sheet: str | None = None
    phonetics_sheet: str | None = None
    script_sheet: str | None = None
    grammar_sheet: str | None = None
    sheets: list[TranslatorContextSheet] = Field(default_factory=list)


class ImageGenerationRequest(BaseModel):
    entity_name: str
    entity_type: str = "spell"
    style: str = "cinematic concept art"
    description: str = ""
    provider: str = "chatgpt"
    dry_run: bool = True


class ImageGenerationResponse(BaseModel):
    provider: str
    status: str
    reason: str | None = None
    dry_run: bool
    prompt: str
    output_path: str
    image_url: str | None = None


class AppSettingsResponse(BaseModel):
    settings: dict[str, Any]


class AppSettingsUpdateRequest(BaseModel):
    patch: dict[str, Any]


class SheetColumnSettingsRequest(BaseModel):
    source: str
    sheet: str
    visible_columns: list[str]


class ValidationCatalogResponse(BaseModel):
    source: str
    sheets: list[str]
    options_by_field: dict[str, dict[str, Any]]
    options_by_sheet: dict[str, dict[str, list[str]]]


class MoneyCatalogResponse(BaseModel):
    source: str
    money_sheet: str | None = None
    matrix_sheet: str | None = None
    currencies: list[str] = Field(default_factory=list)
    matrix: dict[str, dict[str, float]] = Field(default_factory=dict)


class TimelineCalendarMonth(BaseModel):
    row_number: int = Field(ge=1)
    month_order: str | None = None
    month_name: str | None = None
    description: str | None = None
    chore_name: str | None = None
    chore_description: str | None = None
    deity_name: str | None = None
    domain: str | None = None


class TimelineNamingGroup(BaseModel):
    key: str
    label: str
    values: list[str] = Field(default_factory=list)


class TimelineHoliday(BaseModel):
    row_number: int | None = Field(default=None, ge=1)
    name: str
    month_name: str | None = None
    day: int | None = Field(default=None, ge=1)
    recurrence: str | None = None
    source: str | None = None


class TimelineEraEvent(BaseModel):
    year: int | None = None
    era: str | None = None
    event: str
    row_number: int | None = None
    column: int | None = None


class TimelinePresentDay(BaseModel):
    weekday: str | None = None
    day: int | None = None
    event: str | None = None


class TimelinePresentWeek(BaseModel):
    week_index: int | None = None
    days: list[TimelinePresentDay] = Field(default_factory=list)


class TimelinePresentMonth(BaseModel):
    row_start: int | None = Field(default=None, ge=1)
    column_start: int | None = Field(default=None, ge=1)
    year_name: str | None = None
    month_name: str | None = None
    weekdays: list[str] = Field(default_factory=list)
    weeks: list[TimelinePresentWeek] = Field(default_factory=list)
    day_count: int | None = None


class TimelineCatalogResponse(BaseModel):
    source: str
    calendar_months: list[TimelineCalendarMonth] = Field(default_factory=list)
    naming_groups: list[TimelineNamingGroup] = Field(default_factory=list)
    naming_template: str | None = None
    weekdays: list[str] = Field(default_factory=list)
    holidays: list[TimelineHoliday] = Field(default_factory=list)
    era_events: list[TimelineEraEvent] = Field(default_factory=list)
    present_months: list[TimelinePresentMonth] = Field(default_factory=list)
    summary: dict[str, int] = Field(default_factory=dict)


class TimelineCatalogUpdateRequest(BaseModel):
    source: str = "auto"
    calendar_months: list[TimelineCalendarMonth] | None = None
    naming_groups: list[TimelineNamingGroup] | None = None
    weekdays: list[str] | None = None
    holidays: list[TimelineHoliday] | None = None
    era_events: list[TimelineEraEvent] | None = None
