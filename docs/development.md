# Development

## Environment setup

```bash
uv sync --all-extras
```

## Quality checks

```bash
uv run ruff check .
uv run ruff format --check .
uv run pytest
```

## Local CLI smoke checks

```bash
uv run baseliner --version
uv run baseliner scan
```

## CI

CI is defined in `.github/workflows/ci.yml` and runs:

- lint (`ruff check`)
- format check (`ruff format --check`)
- tests (`pytest --cov=baseliner`)

## Pre-commit

The repository includes `.pre-commit-config.yaml` with Ruff and basic hygiene hooks.
