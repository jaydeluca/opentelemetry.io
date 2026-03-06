"""Integration tests for npm formatting and repository root discovery."""

import subprocess
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

import pytest


# Import will fail initially - this is expected for RED phase
try:
    from declarative_configuration_sync.main import find_repo_root, run_npm_formatter
except ImportError:
    pytest.skip("main.py not yet implemented", allow_module_level=True)


class TestFindRepoRoot:
    """Tests for find_repo_root() function."""

    def test_finds_repo_root_from_current_dir(self, tmp_path: Path) -> None:
        """Test 1: find_repo_root() finds repo root by searching for Hugo indicators."""
        # Create Hugo directory structure
        repo_root = tmp_path / "opentelemetry.io"
        repo_root.mkdir()
        (repo_root / "config" / "_default").mkdir(parents=True)
        (repo_root / "content" / "en").mkdir(parents=True)

        # Change to repo root and find it
        import os

        original_cwd = Path.cwd()
        try:
            os.chdir(repo_root)
            result = find_repo_root()
            assert result == repo_root
        finally:
            os.chdir(original_cwd)

    def test_finds_repo_root_from_subdirectory(self, tmp_path: Path) -> None:
        """Test find_repo_root() from nested subdirectory."""
        # Create Hugo directory structure
        repo_root = tmp_path / "opentelemetry.io"
        repo_root.mkdir()
        (repo_root / "config" / "_default").mkdir(parents=True)
        (repo_root / "content" / "en").mkdir(parents=True)

        # Create nested subdirectory
        subdir = repo_root / "scripts" / "declarative-configuration-sync" / "tests"
        subdir.mkdir(parents=True)

        # Change to subdirectory and find root
        import os

        original_cwd = Path.cwd()
        try:
            os.chdir(subdir)
            result = find_repo_root()
            assert result == repo_root
        finally:
            os.chdir(original_cwd)

    def test_raises_error_when_not_in_repo(self, tmp_path: Path) -> None:
        """Test 2: find_repo_root() raises RuntimeError if not in opentelemetry.io repo."""
        # Create directory without Hugo indicators
        not_repo = tmp_path / "not-a-repo"
        not_repo.mkdir()

        import os

        original_cwd = Path.cwd()
        try:
            os.chdir(not_repo)
            with pytest.raises(RuntimeError, match="Could not find opentelemetry.io repository root"):
                find_repo_root()
        finally:
            os.chdir(original_cwd)


class TestRunNpmFormatter:
    """Tests for run_npm_formatter() function."""

    def test_calls_npm_run_fix_format(self, tmp_path: Path) -> None:
        """Test 3: run_npm_formatter() calls subprocess.run with npm fix:format."""
        mock_result = Mock()
        mock_result.returncode = 0

        with patch("subprocess.run", return_value=mock_result) as mock_run:
            result = run_npm_formatter(tmp_path)

            # Verify npm command was called
            mock_run.assert_called_once()
            call_args = mock_run.call_args

            # Check command
            assert call_args[0][0] == ["npm", "run", "fix:format"]

            # Check return value
            assert result is True

    def test_uses_cwd_parameter(self, tmp_path: Path) -> None:
        """Test 4: run_npm_formatter() uses cwd parameter pointing to repo root."""
        mock_result = Mock()
        mock_result.returncode = 0

        with patch("subprocess.run", return_value=mock_result) as mock_run:
            run_npm_formatter(tmp_path)

            # Verify cwd was set correctly
            call_args = mock_run.call_args
            assert call_args[1]["cwd"] == tmp_path

    def test_returns_true_on_success(self, tmp_path: Path) -> None:
        """Test 5: run_npm_formatter() returns True when npm command succeeds."""
        mock_result = Mock()
        mock_result.returncode = 0

        with patch("subprocess.run", return_value=mock_result):
            result = run_npm_formatter(tmp_path)
            assert result is True

    def test_returns_false_on_failure(self, tmp_path: Path) -> None:
        """Test 6: run_npm_formatter() returns False when npm command fails."""
        mock_result = Mock()
        mock_result.returncode = 1
        mock_result.stderr = "npm error"

        with patch("subprocess.run", return_value=mock_result):
            result = run_npm_formatter(tmp_path)
            assert result is False

    def test_handles_timeout_exception(self, tmp_path: Path) -> None:
        """Test 7: run_npm_formatter() handles subprocess.TimeoutExpired exception."""
        with patch("subprocess.run", side_effect=subprocess.TimeoutExpired("npm", 300)):
            result = run_npm_formatter(tmp_path)
            assert result is False

    def test_handles_file_not_found_exception(self, tmp_path: Path) -> None:
        """Test 8: run_npm_formatter() handles FileNotFoundError (npm not installed)."""
        with patch("subprocess.run", side_effect=FileNotFoundError("npm not found")):
            result = run_npm_formatter(tmp_path)
            assert result is False

    def test_handles_generic_exception(self, tmp_path: Path) -> None:
        """Test run_npm_formatter() handles generic exceptions."""
        with patch("subprocess.run", side_effect=Exception("Unexpected error")):
            result = run_npm_formatter(tmp_path)
            assert result is False
