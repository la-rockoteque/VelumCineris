# Target Architecture

## Goals
- One canonical data access layer for spreadsheets and workbook-like sources.
- One canonical domain layer (`models`) shared by all projects.
- Project apps (`FiveETools`, `DNDBeyond`, `Homebrewery`, `Book`, `Spreadsheet`) consume shared layers instead of re-implementing them.
- Stable boundaries between layers so refactors are low-risk.
- Transitional facades and public app-to-app APIs are documented explicitly instead of being treated as already removed.

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
- Public facade: `/Users/rocko/dev/Perso/VelumCineris/Spreadsheet/sheets.py`
- Implementation: `/Users/rocko/dev/Perso/VelumCineris/Spreadsheet/core/Helpers/sheets.py`
- `/Users/rocko/dev/Perso/VelumCineris/Spreadsheet/core/workbook_models/providers.py`

Responsibilities:
- Google Sheets and offline file providers.
- Unified read/write interface for sheet data.
- Shared caching and credentials resolution behavior.
- Stable public import surface for app code while lower-level helpers continue to consolidate.

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
- If one app must consume another app's content assembly, it must use an explicit public adapter API rather than importing sibling `core.*` internals directly.

Allowed imports:
- `models.*`
- `Spreadsheet.sheets`
- `Spreadsheet.core.converters` where ingestion is needed
- Public sibling adapter surfaces when intentionally exposed (currently `FiveETools.datasets`)

### 5) Compatibility Layer (temporary)
Status:
- Still active during the current consolidation pass.

Current facades in use:
- `/Users/rocko/dev/Perso/VelumCineris/Spreadsheet/sheets.py`
- `/Users/rocko/dev/Perso/VelumCineris/Spreadsheet/sources.py`
- `/Users/rocko/dev/Perso/VelumCineris/Book/book_api.py`
- `/Users/rocko/dev/Perso/VelumCineris/Book/google_docs_client.py`
- `/Users/rocko/dev/Perso/VelumCineris/Book/styles.py`
- `/Users/rocko/dev/Perso/VelumCineris/DNDBeyond/helpers`
- `/Users/rocko/dev/Perso/VelumCineris/WorldAnvil/WorldAnvilAPI.py`
- `/Users/rocko/dev/Perso/VelumCineris/Homebrewery/*.py` helper facades

## Dependency Direction
Allowed direction:
- Domain <- Data <- Ingestion <- Apps

Forbidden direction:
- Domain -> Apps
- Data -> Apps
- Shared layers importing app modules
- App adapters importing sibling app internals such as `FiveETools.core.*`

## Naming and Pattern Conventions
- `*Client`: external systems access.
- `*Provider`: low-level source adapters.
- `*Converter` / `*Mapper`: transformations between representations.
- `*Model`: domain-level Pydantic entities.
- Keep source tab IDs in one place (sheet registries), not scattered literals.

## Definition of Done for Consolidation
- All Google Sheet reads/writes flow through the public spreadsheet facade at `/Users/rocko/dev/Perso/VelumCineris/Spreadsheet/sheets.py`.
- No direct `pd.read_csv("https://docs.google.com/spreadsheets/...export?format=csv...")` in app code.
- No duplicate client implementations.
- Import boundary check is green in strict mode.
- Adapter layers use public sibling APIs, not sibling `core.*` packages.
