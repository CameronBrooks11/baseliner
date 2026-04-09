from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from github import UnknownObjectException

from baseliner.actions.github_issues import ISSUE_TITLE, GitHubIssueAction
from baseliner.models.result import RepoResult


def _missing_label_exception() -> UnknownObjectException:
    return UnknownObjectException(404, {"message": "Not Found"}, None)


@pytest.fixture
def mock_issue() -> MagicMock:
    issue = MagicMock()
    issue.number = 7
    issue.title = ISSUE_TITLE
    return issue


@pytest.fixture
def mock_repo(mock_issue: MagicMock) -> MagicMock:
    repo = MagicMock()
    repo.full_name = "test-org/my-repo"
    repo.get_label.side_effect = _missing_label_exception()
    repo.create_label.return_value = MagicMock(name="label")
    repo.get_issues.return_value = []
    repo.create_issue.return_value = mock_issue
    return repo


def test_creates_new_issue_when_none_exists(
    mock_repo: MagicMock,
    sample_repo_result: RepoResult,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr("baseliner.actions.github_issues.time.sleep", lambda *_: None)

    action = GitHubIssueAction(token="fake", dry_run=False)
    action.run(sample_repo_result, mock_repo)

    mock_repo.create_issue.assert_called_once()
    call_kwargs = mock_repo.create_issue.call_args.kwargs
    assert call_kwargs["title"] == ISSUE_TITLE
    assert "baseliner findings" in call_kwargs["body"]
    assert call_kwargs["labels"] == [mock_repo.create_label.return_value]


def test_updates_existing_issue(
    mock_repo: MagicMock,
    mock_issue: MagicMock,
    sample_repo_result: RepoResult,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr("baseliner.actions.github_issues.time.sleep", lambda *_: None)
    mock_repo.get_issues.return_value = [mock_issue]

    action = GitHubIssueAction(token="fake", dry_run=False)
    action.run(sample_repo_result, mock_repo)

    mock_repo.create_issue.assert_not_called()
    mock_issue.edit.assert_called_once()


def test_dry_run_makes_no_write_api_calls(
    mock_repo: MagicMock,
    sample_repo_result: RepoResult,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sleep_calls = []
    monkeypatch.setattr(
        "baseliner.actions.github_issues.time.sleep",
        lambda *_: sleep_calls.append("sleep"),
    )

    action = GitHubIssueAction(token="fake", dry_run=True)
    action.run(sample_repo_result, mock_repo)

    mock_repo.create_issue.assert_not_called()
    mock_repo.create_label.assert_not_called()
    assert sleep_calls == []


def test_reuses_existing_label(
    mock_repo: MagicMock,
    sample_repo_result: RepoResult,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr("baseliner.actions.github_issues.time.sleep", lambda *_: None)
    existing_label = MagicMock(name="existing-label")
    mock_repo.get_label.side_effect = None
    mock_repo.get_label.return_value = existing_label

    action = GitHubIssueAction(token="fake", dry_run=False)
    action.run(sample_repo_result, mock_repo)

    mock_repo.create_label.assert_not_called()


def test_issue_body_contains_expected_sections(
    sample_repo_result: RepoResult,
) -> None:
    action = GitHubIssueAction(token="fake", dry_run=True)
    body = action._build_body(sample_repo_result)

    assert "## baseliner findings" in body
    assert "Score" in body
    assert "managed by" in body
    assert "baseliner" in body
    for result in sample_repo_result.results:
        assert result.check_id in body
