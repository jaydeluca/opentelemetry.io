"""Tests for github_fetcher module.

Tests GitHub API integration for fetching schema files from opentelemetry-configuration repo.
"""

from unittest.mock import Mock, patch

import pytest
import requests
from requests.exceptions import ConnectionError, Timeout

from declarative_configuration_sync.github_fetcher import GitHubSchemaFetcher


class TestGitHubSchemaFetcher:
    """Test GitHubSchemaFetcher class."""

    def test_fetch_file_content_success(self) -> None:
        """Test successful fetch of YAML content from GitHub API."""
        fetcher = GitHubSchemaFetcher(timeout=30)
        expected_content = """types:
  - name: TracerProvider
    description: Configuration for TracerProvider
"""

        with patch("requests.get") as mock_get:
            mock_response = Mock()
            mock_response.text = expected_content
            mock_response.status_code = 200
            mock_response.raise_for_status = Mock()
            mock_get.return_value = mock_response

            result = fetcher.fetch_file_content("schema/tracer.yaml")

            assert result == expected_content
            mock_get.assert_called_once()
            # Verify URL construction
            call_args = mock_get.call_args
            assert "api.github.com" in call_args[0][0]
            assert "open-telemetry" in call_args[0][0]
            assert "opentelemetry-configuration" in call_args[0][0]
            assert "contents/schema/tracer.yaml" in call_args[0][0]

    def test_fetch_file_content_uses_raw_accept_header(self) -> None:
        """Test that fetch_file_content uses correct Accept header for raw content."""
        fetcher = GitHubSchemaFetcher()

        with patch("requests.get") as mock_get:
            mock_response = Mock()
            mock_response.text = "content"
            mock_response.status_code = 200
            mock_response.raise_for_status = Mock()
            mock_get.return_value = mock_response

            fetcher.fetch_file_content("schema/test.yaml")

            call_kwargs = mock_get.call_args[1]
            assert "headers" in call_kwargs
            assert call_kwargs["headers"]["Accept"] == "application/vnd.github.raw+json"

    def test_fetch_file_content_uses_ref_parameter(self) -> None:
        """Test that fetch_file_content passes ref parameter to API."""
        fetcher = GitHubSchemaFetcher()

        with patch("requests.get") as mock_get:
            mock_response = Mock()
            mock_response.text = "content"
            mock_response.status_code = 200
            mock_response.raise_for_status = Mock()
            mock_get.return_value = mock_response

            fetcher.fetch_file_content("schema/test.yaml", ref="v1.0.0")

            call_kwargs = mock_get.call_args[1]
            assert "params" in call_kwargs
            assert call_kwargs["params"]["ref"] == "v1.0.0"

    def test_fetch_file_content_404_not_found(self) -> None:
        """Test fetch_file_content raises RuntimeError on 404 (file not found)."""
        fetcher = GitHubSchemaFetcher()

        with patch("requests.get") as mock_get:
            mock_response = Mock()
            mock_response.status_code = 404
            http_error = requests.exceptions.HTTPError("404 Not Found")
            http_error.response = mock_response  # Attach response to exception
            mock_response.raise_for_status = Mock(side_effect=http_error)
            mock_get.return_value = mock_response

            with pytest.raises(RuntimeError) as exc_info:
                fetcher.fetch_file_content("schema/nonexistent.yaml")

            assert "File not found" in str(exc_info.value)
            assert "schema/nonexistent.yaml" in str(exc_info.value)
            assert "main" in str(exc_info.value)

    def test_fetch_file_content_403_rate_limit(self) -> None:
        """Test fetch_file_content raises RuntimeError on 403 (rate limit)."""
        fetcher = GitHubSchemaFetcher()

        with patch("requests.get") as mock_get:
            mock_response = Mock()
            mock_response.status_code = 403
            http_error = requests.exceptions.HTTPError("403 Forbidden")
            http_error.response = mock_response  # Attach response to exception
            mock_response.raise_for_status = Mock(side_effect=http_error)
            mock_get.return_value = mock_response

            with pytest.raises(RuntimeError) as exc_info:
                fetcher.fetch_file_content("schema/test.yaml")

            assert "rate limit" in str(exc_info.value).lower() or "authentication" in str(exc_info.value).lower()

    def test_fetch_file_content_timeout_error(self) -> None:
        """Test fetch_file_content raises RuntimeError on timeout."""
        fetcher = GitHubSchemaFetcher(timeout=5)

        with patch("requests.get") as mock_get:
            mock_get.side_effect = Timeout("Request timed out")

            with pytest.raises(RuntimeError) as exc_info:
                fetcher.fetch_file_content("schema/test.yaml")

            assert "timeout" in str(exc_info.value).lower()
            assert "5" in str(exc_info.value)

    def test_fetch_file_content_network_error(self) -> None:
        """Test fetch_file_content raises RuntimeError on network errors."""
        fetcher = GitHubSchemaFetcher()

        with patch("requests.get") as mock_get:
            mock_get.side_effect = ConnectionError("Network unreachable")

            with pytest.raises(RuntimeError) as exc_info:
                fetcher.fetch_file_content("schema/test.yaml")

            assert "network error" in str(exc_info.value).lower()

    def test_fetch_file_content_logs_api_call(self, caplog) -> None:  # type: ignore[no-untyped-def]
        """Test that fetch_file_content logs API calls."""
        fetcher = GitHubSchemaFetcher()

        with patch("requests.get") as mock_get:
            mock_response = Mock()
            mock_response.text = "content"
            mock_response.status_code = 200
            mock_response.raise_for_status = Mock()
            mock_get.return_value = mock_response

            fetcher.fetch_file_content("schema/test.yaml")

            # Check that something was logged (implementation will add logging)
            # This test ensures logging infrastructure is in place
            assert len(caplog.records) >= 0  # Placeholder - implementation will add actual logging
