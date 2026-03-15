# Homebrewery

Generate Homebrewery-ready markdown from Velum Cineris content.

## Quick Start

```bash
# Export markdown for modern spells (limited sample)
poetry run python -m Homebrewery.cli export-markdown --entity spell --setting modern --limit 10
```

## Architecture

```
Homebrewery/
├── cli.py                      # Normalized CLI entrypoint
├── datasets/                   # Entity loading adapters
├── mappers/                    # Markdown mapping adapters
├── services/                   # Markdown build orchestration
├── exports/                    # Markdown file output helpers
├── core/Helpers/               # Legacy canonical helpers
├── core/style/                 # CSS/theme assets
├── core/markdown/              # Generated markdown artifacts
└── tests/
```
