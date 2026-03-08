# Target Architecture

## Goals
- One canonical data access layer for spreadsheets and workbook-like sources.
- One canonical domain layer (`models`) shared by all projects.
- Project apps (`FiveETools`, `DNDBeyond`, `Homebrewery`, `Book`, `Spreadsheet`) consume shared layers instead of re-implementing them.
- Stable boundaries between layers so refactors are low-risk.

## Layers

### 1) Domain Layer
Location:
- `/Users/rocko/dev/Perso/VelumCineris/models`

Responsibilities:
- Core Pydantic domain models.
- Shared field models and domain invariants.
- No dependency on project-specific DTO/export formats.

Allowed imports:
- Standard library
- Third-party libs
- `models.*`

Disallowed imports:
- `FiveETools.*`, `DNDBeyond.*`, `Homebrewery.*`, `Book.*`

### 2) Data Access Layer
Location:
- `/Users/rocko/dev/Perso/VelumCineris/Spreadsheet/sheets.py`
- `/Users/rocko/dev/Perso/VelumCineris/Spreadsheet/core/workbook_models/providers.py`

Responsibilities:
- Google Sheets and offline file providers.
- Unified read/write interface for sheet data.
- Shared caching and credentials resolution behavior.

Allowed imports:
- Standard library
- Third-party libs
- `Spreadsheet.*` (data infrastructure only)

Disallowed imports:
- App-specific pipelines and DTO mappers.

### 3) Ingestion/Mapping Layer
Location:
- `/Users/rocko/dev/Perso/VelumCineris/Spreadsheet/core/converters`
- `/Users/rocko/dev/Perso/VelumCineris/Spreadsheet/core/workbook_models`

Responsibilities:
- Convert tabular sheet data to domain models.
- Apply validation catalog rules.
- Attach virtual relations between model sets.

Allowed imports:
- `Spreadsheet.sheets`
- `models.*`

### 4) App Adapter Layers
Locations:
- `/Users/rocko/dev/Perso/VelumCineris/FiveETools`
- `/Users/rocko/dev/Perso/VelumCineris/DNDBeyond`
- `/Users/rocko/dev/Perso/VelumCineris/Homebrewery`
- `/Users/rocko/dev/Perso/VelumCineris/Book`

Responsibilities:
- Project-specific DTO assembly and export format generation.
- Project-specific API integrations.
- No duplicate data-access clients.

Allowed imports:
- `models.*`
- `Spreadsheet.sheets`
- `Spreadsheet.core.converters` where ingestion is needed

### 5) Compatibility Layer (temporary)
Locations:
- `/Users/rocko/dev/Perso/VelumCineris/FiveETools/gsheets_client.py`
- `/Users/rocko/dev/Perso/VelumCineris/Spreadsheet/core/translator/gsheets_client.py`
- `/Users/rocko/dev/Perso/VelumCineris/models/converters/*`
- `/Users/rocko/dev/Perso/VelumCineris/Spreadsheet/models/converters/*`

Responsibilities:
- Preserve existing imports while migration completes.
- Must only re-export canonical implementations.

## Dependency Direction
Allowed direction:
- Domain <- Data <- Ingestion <- Apps

Forbidden direction:
- Domain -> Apps
- Data -> Apps
- Shared layers importing app modules

## Naming and Pattern Conventions
- `*Client`: external systems access.
- `*Provider`: low-level source adapters.
- `*Converter` / `*Mapper`: transformations between representations.
- `*Model`: domain-level Pydantic entities.
- Keep source tab IDs in one place (sheet registries), not scattered literals.

## Definition of Done for Consolidation
- All Google Sheet reads/writes flow through `/Users/rocko/dev/Perso/VelumCineris/Spreadsheet/sheets.py`.
- No direct `pd.read_csv("https://docs.google.com/spreadsheets/...export?format=csv...")` in app code.
- No duplicate client implementations outside compatibility wrappers.
- Import boundary check is green in strict mode.
