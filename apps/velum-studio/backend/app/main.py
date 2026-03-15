from __future__ import annotations

import csv
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from .config import settings
from .schemas import (
    AppSettingsResponse,
    AppSettingsUpdateRequest,
    BookFormatterRequest,
    BookFormatterResponse,
    FormatterStyleTemplateResponse,
    FormatterStyleTemplatesResponse,
    ImageGenerationRequest,
    ImageGenerationResponse,
    IntegrationListResponse,
    IntegrationPreviewRequest,
    IntegrationPreviewResponse,
    IntegrationStatusResponse,
    IntegrationSyncRequest,
    IntegrationSyncResponse,
    IntelligenceRequest,
    IntelligenceResponse,
    LoadingTriviaItem,
    LoadingTriviaResponse,
    ItemActionRequest,
    ItemActionResponse,
    MoneyCatalogResponse,
    SourceInfo,
    SpreadsheetRowResponse,
    SpreadsheetRowsResponse,
    SpreadsheetSheetSchemaResponse,
    SpreadsheetSheetsResponse,
    SpreadsheetSourcesResponse,
    TimelineCatalogResponse,
    TimelineCatalogUpdateRequest,
    ValidationCatalogResponse,
    SheetColumnSettingsRequest,
    TranslatorRequest,
    TranslatorContextResponse,
    TranslatorResponse,
    TranslatorTargetsResponse,
)
from .services.book_formatter_service import BookFormatterService
from .services.formatter_style_service import FormatterStyleService
from .services.image_generator_service import ImageGeneratorService
from .services.integration_service import IntegrationManager
from .services.intelligence_service import IntelligenceService
from .services.settings_service import SettingsService
from .services.spreadsheet_service import RegistryManager, SpreadsheetRuntimeConfig
from .services.timeline_service import TimelineService
from .services.translator_service import TranslatorService


runtime = SpreadsheetRuntimeConfig(
    spreadsheet_id=settings.spreadsheet_id,
    xlsx_path=settings.xlsx_path,
    credentials_path=settings.credentials_path,
)
registry_manager = RegistryManager(runtime)
integration_manager = IntegrationManager(registry_manager)
book_formatter_service = BookFormatterService()
formatter_style_service = FormatterStyleService(Path(__file__).resolve().parents[4] / "Homebrewery/core/style")
intelligence_service = IntelligenceService()
translator_service = TranslatorService(registry_manager)
image_generator_service = ImageGeneratorService()
settings_service = SettingsService(settings.settings_path)
timeline_service = TimelineService(
    timeline_xlsx_path=settings.timeline_xlsx_path,
    timeline_spreadsheet_id=settings.timeline_spreadsheet_id,
    credentials_path=settings.credentials_path,
)

app = FastAPI(title="Velum Studio API", version="0.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/loading-trivia", response_model=LoadingTriviaResponse)
def loading_trivia() -> LoadingTriviaResponse:
    trivia_path = settings.assets_path / "loading_trivia.csv"
    if not trivia_path.exists():
        return LoadingTriviaResponse(items=[])

    items: list[LoadingTriviaItem] = []
    try:
        with trivia_path.open("r", newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                tidbit = str(row.get("tidbit", "")).strip()
                if not tidbit:
                    continue
                items.append(
                    LoadingTriviaItem(
                        tidbit=tidbit,
                        entity_type=(str(row.get("entity_type", "")).strip() or None),
                        entity_name=(str(row.get("entity_name", "")).strip() or None),
                        source=(str(row.get("source", "")).strip() or None),
                    )
                )
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to read loading trivia CSV: {exc}",
        ) from exc

    return LoadingTriviaResponse(items=items)


@app.get("/api/settings", response_model=AppSettingsResponse)
def get_settings() -> AppSettingsResponse:
    try:
        payload = settings_service.get()
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return AppSettingsResponse(settings=payload)


@app.put("/api/settings", response_model=AppSettingsResponse)
def update_settings(body: AppSettingsUpdateRequest) -> AppSettingsResponse:
    try:
        payload = settings_service.update(body.patch)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return AppSettingsResponse(settings=payload)


@app.put("/api/settings/columns", response_model=AppSettingsResponse)
def set_sheet_columns(body: SheetColumnSettingsRequest) -> AppSettingsResponse:
    try:
        payload = settings_service.set_sheet_columns(
            source=body.source,
            sheet=body.sheet,
            visible_columns=body.visible_columns,
        )
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return AppSettingsResponse(settings=payload)


@app.delete("/api/settings/columns", response_model=AppSettingsResponse)
def reset_sheet_columns(
    source: str = Query(...),
    sheet: str = Query(...),
) -> AppSettingsResponse:
    try:
        payload = settings_service.reset_sheet_columns(source=source, sheet=sheet)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return AppSettingsResponse(settings=payload)


@app.get("/api/spreadsheet/sources", response_model=SpreadsheetSourcesResponse)
def spreadsheet_sources() -> SpreadsheetSourcesResponse:
    source_flags = registry_manager.available_sources()
    sources = [
        SourceInfo(source=source, available=available, reason=reason)
        for source, (available, reason) in source_flags.items()
    ]

    default_source = "auto"
    if not source_flags["auto"][0]:
        default_source = "xlsx" if source_flags["xlsx"][0] else "google"

    return SpreadsheetSourcesResponse(default_source=default_source, sources=sources)


@app.get("/api/spreadsheet/sheets", response_model=SpreadsheetSheetsResponse)
def spreadsheet_sheets(source: str = Query(default="auto")) -> SpreadsheetSheetsResponse:
    try:
        sheets = registry_manager.list_sheets(source)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return SpreadsheetSheetsResponse(source=source, sheets=sheets)


@app.get("/api/compendium/sheets", response_model=SpreadsheetSheetsResponse)
def compendium_sheets(source: str = Query(default="auto")) -> SpreadsheetSheetsResponse:
    try:
        sheets = registry_manager.list_compendium_sheets(source)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return SpreadsheetSheetsResponse(source=source, sheets=sheets)


@app.get("/api/validations/sheets", response_model=SpreadsheetSheetsResponse)
def validation_sheets(source: str = Query(default="auto")) -> SpreadsheetSheetsResponse:
    try:
        sheets = registry_manager.list_validation_sheets(source)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return SpreadsheetSheetsResponse(source=source, sheets=sheets)


@app.get("/api/validations/catalog", response_model=ValidationCatalogResponse)
def validation_catalog(source: str = Query(default="auto")) -> ValidationCatalogResponse:
    try:
        payload = registry_manager.validation_catalog(source)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return ValidationCatalogResponse(
        source=source,
        sheets=payload["sheets"],
        options_by_field=payload["options_by_field"],
        options_by_sheet=payload["options_by_sheet"],
    )


@app.get("/api/spreadsheet/schema", response_model=SpreadsheetSheetSchemaResponse)
def spreadsheet_schema(
    source: str = Query(default="auto"),
    sheet: str = Query(...),
) -> SpreadsheetSheetSchemaResponse:
    try:
        columns, header_row, is_validation_sheet, validation_columns = registry_manager.schema_for(source, sheet)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"Unknown sheet '{sheet}'") from exc
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return SpreadsheetSheetSchemaResponse(
        source=source,
        sheet=sheet,
        header_row=header_row,
        is_validation_sheet=is_validation_sheet,
        columns=columns,
        validation_columns=validation_columns,
    )


@app.get("/api/spreadsheet/rows", response_model=SpreadsheetRowsResponse)
def spreadsheet_rows(
    source: str = Query(default="auto"),
    sheet: str = Query(...),
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    q: str | None = Query(default=None),
) -> SpreadsheetRowsResponse:
    try:
        columns, rows, total = registry_manager.rows_for(
            source,
            sheet,
            offset=offset,
            limit=limit,
            query=q,
        )
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"Unknown sheet '{sheet}'") from exc
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return SpreadsheetRowsResponse(
        source=source,
        sheet=sheet,
        offset=offset,
        limit=limit,
        total_rows=total,
        columns=columns,
        rows=rows,
    )


@app.get("/api/spreadsheet/row", response_model=SpreadsheetRowResponse)
def spreadsheet_row(
    source: str = Query(default="auto"),
    sheet: str = Query(...),
    row_number: int = Query(..., ge=1),
) -> SpreadsheetRowResponse:
    try:
        columns, row, header_row = registry_manager.row_for(source, sheet, row_number=row_number)
        sections = registry_manager.row_sections_for(source, sheet, row)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return SpreadsheetRowResponse(
        source=source,
        sheet=sheet,
        row_number=row_number,
        header_row=header_row,
        columns=columns,
        row=row,
        sections=sections,
    )


@app.get("/api/integrations", response_model=IntegrationListResponse)
def list_integrations() -> IntegrationListResponse:
    try:
        integrations = integration_manager.list_cards(source="auto")
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return IntegrationListResponse(integrations=integrations)


@app.get("/api/integrations/{integration_key}/status", response_model=IntegrationStatusResponse)
def integration_status(
    integration_key: str,
    source: str = Query(default="auto"),
) -> IntegrationStatusResponse:
    try:
        payload = integration_manager.status(integration_key, source=source)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"Unknown integration '{integration_key}'") from exc
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return IntegrationStatusResponse.model_validate(payload)


@app.post("/api/integrations/{integration_key}/preview", response_model=IntegrationPreviewResponse)
def integration_preview(
    integration_key: str,
    body: IntegrationPreviewRequest,
) -> IntegrationPreviewResponse:
    try:
        payload = integration_manager.preview(
            integration_key,
            source=body.source,
            limit_per_sheet=body.limit_per_sheet,
            include_samples=body.include_samples,
        )
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"Unknown integration '{integration_key}'") from exc
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return IntegrationPreviewResponse.model_validate(payload)


@app.post("/api/integrations/{integration_key}/sync", response_model=IntegrationSyncResponse)
def integration_sync(
    integration_key: str,
    body: IntegrationSyncRequest,
) -> IntegrationSyncResponse:
    try:
        payload = integration_manager.sync(
            integration_key,
            source=body.source,
            dry_run=body.dry_run,
            limit_per_sheet=body.limit_per_sheet,
            include_samples=body.include_samples,
        )
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"Unknown integration '{integration_key}'") from exc
    except NotImplementedError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return IntegrationSyncResponse.model_validate(payload)


@app.post("/api/items/{integration_key}/action", response_model=ItemActionResponse)
def item_action(
    integration_key: str,
    body: ItemActionRequest,
) -> ItemActionResponse:
    try:
        _, row, _ = registry_manager.row_for(body.source, body.sheet, row_number=body.row_number)
        payload = integration_manager.item_action(
            integration_key,
            source=body.source,
            sheet_name=body.sheet,
            row_number=body.row_number,
            row_data=row,
            requested_operation=body.operation,
            dry_run=body.dry_run,
        )
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return ItemActionResponse.model_validate(payload)


@app.post("/api/book-formatter/preview", response_model=BookFormatterResponse)
def book_formatter_preview(body: BookFormatterRequest) -> BookFormatterResponse:
    try:
        _, row, _ = registry_manager.row_for(body.source, body.sheet, row_number=body.row_number)
        payload = book_formatter_service.preview(
            sheet=body.sheet,
            row_number=body.row_number,
            row_data=row,
            targets=body.targets,
            style_template=body.style_template,
            style_css=body.style_css,
        )
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return BookFormatterResponse.model_validate(payload)


@app.get("/api/formatter/styles", response_model=FormatterStyleTemplatesResponse)
def formatter_style_templates() -> FormatterStyleTemplatesResponse:
    try:
        templates = formatter_style_service.list_templates()
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return FormatterStyleTemplatesResponse(templates=templates)


@app.get("/api/formatter/styles/template", response_model=FormatterStyleTemplateResponse)
def formatter_style_template(name: str = Query(...)) -> FormatterStyleTemplateResponse:
    try:
        payload = formatter_style_service.load_template(name)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return FormatterStyleTemplateResponse.model_validate(payload)


@app.post("/api/intelligence/suggest", response_model=IntelligenceResponse)
def intelligence_suggest(body: IntelligenceRequest) -> IntelligenceResponse:
    try:
        payload = intelligence_service.suggest(
            mode=body.mode,
            instruction=body.instruction,
            row_data=body.row_data,
            use_local_llm=body.use_local_llm,
            model=body.model,
        )
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return IntelligenceResponse.model_validate(payload)


@app.get("/api/translator/targets", response_model=TranslatorTargetsResponse)
def translator_targets(source: str = Query(default="auto")) -> TranslatorTargetsResponse:
    try:
        targets = translator_service.available_targets(source)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return TranslatorTargetsResponse(source=source, targets=targets)


@app.get("/api/translator/context", response_model=TranslatorContextResponse)
def translator_context(
    source: str = Query(default="auto"),
    target: str = Query(...),
) -> TranslatorContextResponse:
    try:
        payload = translator_service.language_context(source=source, target=target)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return TranslatorContextResponse.model_validate(payload)


@app.post("/api/translator/translate", response_model=TranslatorResponse)
def translator_translate(body: TranslatorRequest) -> TranslatorResponse:
    try:
        payload = translator_service.translate(source=body.source, target=body.target, text=body.text)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return TranslatorResponse.model_validate(payload)


@app.get("/api/money/catalog", response_model=MoneyCatalogResponse)
def money_catalog(source: str = Query(default="auto")) -> MoneyCatalogResponse:
    try:
        payload = registry_manager.money_catalog(source)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return MoneyCatalogResponse(
        source=source,
        money_sheet=payload.get("money_sheet"),
        matrix_sheet=payload.get("matrix_sheet"),
        currencies=payload.get("currencies", []),
        matrix=payload.get("matrix", {}),
    )


@app.get("/api/timeline/catalog", response_model=TimelineCatalogResponse)
def timeline_catalog(source: str = Query(default="auto")) -> TimelineCatalogResponse:
    try:
        payload = timeline_service.load_catalog(source)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return TimelineCatalogResponse.model_validate(payload)


@app.put("/api/timeline/catalog", response_model=TimelineCatalogResponse)
def timeline_save(body: TimelineCatalogUpdateRequest) -> TimelineCatalogResponse:
    try:
        payload = timeline_service.save_catalog(
            body.source,
            calendar_months=[item.model_dump() for item in body.calendar_months] if body.calendar_months is not None else None,
            naming_groups=[item.model_dump() for item in body.naming_groups] if body.naming_groups is not None else None,
            weekdays=body.weekdays,
            holidays=[item.model_dump() for item in body.holidays] if body.holidays is not None else None,
            era_events=[item.model_dump() for item in body.era_events] if body.era_events is not None else None,
        )
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return TimelineCatalogResponse.model_validate(payload)


@app.post("/api/image-generator/generate", response_model=ImageGenerationResponse)
def image_generate(body: ImageGenerationRequest) -> ImageGenerationResponse:
    try:
        payload = image_generator_service.generate(
            entity_name=body.entity_name,
            entity_type=body.entity_type,
            style=body.style,
            description=body.description,
            provider=body.provider,
            dry_run=body.dry_run,
        )
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return ImageGenerationResponse.model_validate(payload)


frontend_dir = Path(__file__).resolve().parents[2] / "frontend"
frontend_dist_dir = frontend_dir / "dist"
if settings.assets_path.exists():
    app.mount("/assets", StaticFiles(directory=settings.assets_path), name="assets")
if frontend_dist_dir.exists():
    app.mount("/app", StaticFiles(directory=frontend_dist_dir, html=True), name="frontend")


@app.get("/")
def root() -> RedirectResponse:
    if frontend_dist_dir.exists():
        return RedirectResponse(url="/app/index.html")
    dev_url = f"http://{settings.host}:5173/app/"
    return RedirectResponse(url=dev_url)
