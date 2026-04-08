# baseliner

`baseliner` is a Python CLI for repository baseline compliance scanning.

## Status

Phase 0 is implemented. Current CLI behavior is intentionally minimal:

- `baseliner --version` prints the package version.
- `baseliner scan` is a stub command that prints `not yet implemented`.

## Requirements

- Python `>=3.12`
- [`uv`](https://docs.astral.sh/uv/)

## Install (from source)

```bash
git clone <your-repo-url>
cd baseliner
uv sync --all-extras
```

## Quick start

```bash
uv run baseliner --version
uv run baseliner scan
```

## Docs

- [Getting Started](docs/getting-started.md)
- [CLI Reference](docs/cli.md)
- [Development](docs/development.md)

## License

MIT. See [LICENSE](LICENSE).
