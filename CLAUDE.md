# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**hdx-python-pipelineutils** is a shared utility library for HDX data pipeline scrapers. It provides reusable components for reading data, resolving admin levels, and looking up sector and org-type codes from YAML-driven configuration.

## Commands

Install dependencies:
```bash
uv sync
```

Run tests:
```bash
uv run pytest
```

Run a single test:
```bash
uv run pytest tests/test_lookup.py
```

Lint check:
```bash
pre-commit run --all-files
```

## Architecture

Source lives under `src/hdx/pipelineutils/`:

- **`reader.py`** — `Read` (subclass of `hdx-python-utilities` `Retrieve`): downloads and caches tabular data (CSV, XLS, XLSX), with save/use-saved modes, date extraction from time periods, and HDX dataset/resource helpers.
- **`lookup.py`** — `Lookup`: base class for YAML-driven code lookups. Loads a configuration YAML, builds normalised name→code mappings, and resolves codes via `hdx-python-country`'s fuzzy matching.
- **`org_type.py`** — `OrgType(Lookup)`: resolves organisation-type codes using `org_type_configuration.yaml`.
- **`sector.py`** — `Sector(Lookup)`: resolves sector codes using `sector_configuration.yaml`.
- **`hapi_admins.py`** — `complete_admins()`: populates adm-level names from p-codes and vice-versa using `hdx-python-country` `AdminLevel` objects; returns the resolved level and a list of warnings.
- **`__init__.py`** — shared helpers: `string_params_to_dict`, `match_template` (extracts `{{...}}` placeholders), `get_startend_dates_from_time_period`.

## Testing

Tests are in `tests/` and use `pytest`. No live HDX connection is required — data is mocked or loaded from `tests/fixtures/`. Coverage is written to `coverage.lcov` and JUnit XML to `test-results.xml`.

## Code Style

Formatted and linted with `ruff` (rules: E, F, I, UP; line-length not enforced). Python ≥ 3.10. Use `X | Y` union syntax (PEP 604), not `Optional`/`Union`. Google-style docstrings with `Args:` and `Returns:` sections.

## Collaboration Style

- Be objective, not agreeable. Act as a partner, not a sycophant. Push back when you disagree, flag tradeoffs honestly, and don't sugarcoat problems.
- Keep explanations brief and to the point.
- Don't rely on recalled knowledge for facts that could be stale (API behaviour, library versions, external systems). Search or read the actual source first.

## Scope of Changes

When fixing a bug or addressing PR feedback, change only what is necessary to resolve the specific issue. Do not refactor surrounding code, rename variables, adjust formatting, or make improvements in the same commit unless they are directly required by the fix.
