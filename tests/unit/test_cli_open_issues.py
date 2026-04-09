from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from baseliner.cli import app


def _write_local_config(path: Path, local_repo_path: Path) -> Path:
    config_path = path / "baseliner.yaml"
    config_path.write_text(
        "\n".join(
            [
                "scope:",
                "  local:",
                "    paths:",
                f"      - {local_repo_path.resolve()}",
                "policy:",
                "  base: default",
            ]
        ),
        encoding="utf-8",
    )
    return config_path


def test_open_issues_missing_token_exits_2(
    tmp_path: Path,
    full_repo_path: Path,
    monkeypatch,
) -> None:
    config_path = _write_local_config(tmp_path, full_repo_path)
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)

    runner = CliRunner()
    result = runner.invoke(
        app,
        ["scan", "--config", str(config_path), "--open-issues", "--format", "table"],
    )

    assert result.exit_code == 2
    assert "--open-issues requires a GitHub token in 'GITHUB_TOKEN'" in result.stderr


def test_open_issues_skips_local_repo_without_github_reference(
    tmp_path: Path,
    full_repo_path: Path,
    monkeypatch,
) -> None:
    config_path = _write_local_config(tmp_path, full_repo_path)
    monkeypatch.setenv("GITHUB_TOKEN", "fake-token")

    runner = CliRunner()
    result = runner.invoke(
        app,
        ["scan", "--config", str(config_path), "--open-issues", "--format", "table"],
    )

    assert result.exit_code == 0
    assert "Cannot open issue for" in result.stderr
