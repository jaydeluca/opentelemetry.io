"""Integration tests for GitHubSchemaFetcher."""

from unittest.mock import Mock, patch

import pytest
import requests

from declarative_configuration_sync.github_fetcher import GitHubSchemaFetcher


class TestFetchLatestRelease:
    """Tests for fetch_latest_release() method."""

    @patch("declarative_configuration_sync.github_fetcher.requests.get")
    def test_fetch_latest_release_returns_tag_name(self, mock_get: Mock) -> None:
        """Test 1: fetch_latest_release() returns tag name string."""
        # Mock GitHub API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"tag_name": "v0.1.0"}
        mock_get.return_value = mock_response

        fetcher = GitHubSchemaFetcher()
        tag = fetcher.fetch_latest_release()

        assert tag == "v0.1.0"
        # Verify correct API endpoint was called
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        assert "releases/latest" in call_args[0][0]

    @patch("declarative_configuration_sync.github_fetcher.requests.get")
    def test_fetch_latest_release_handles_api_errors(self, mock_get: Mock) -> None:
        """Test 2: fetch_latest_release() handles API errors gracefully with RuntimeError."""
        # Mock HTTP error
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()
        mock_get.return_value = mock_response

        fetcher = GitHubSchemaFetcher()

        with pytest.raises(RuntimeError) as exc_info:
            fetcher.fetch_latest_release()

        assert "release" in str(exc_info.value).lower()

    @patch("declarative_configuration_sync.github_fetcher.requests.get")
    def test_fetch_latest_release_uses_github_api_endpoint(
        self, mock_get: Mock
    ) -> None:
        """Test 3: fetch_latest_release() uses correct GitHub API endpoint."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"tag_name": "v0.2.0"}
        mock_get.return_value = mock_response

        fetcher = GitHubSchemaFetcher()
        fetcher.fetch_latest_release()

        # Verify correct endpoint
        call_args = mock_get.call_args
        url = call_args[0][0]
        assert url == "https://api.github.com/repos/open-telemetry/opentelemetry-configuration/releases/latest"

    @patch("declarative_configuration_sync.github_fetcher.requests.get")
    def test_fetch_latest_release_raises_on_missing_tag_name(
        self, mock_get: Mock
    ) -> None:
        """Test 4: fetch_latest_release() raises RuntimeError if tag_name missing."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}  # Missing tag_name
        mock_get.return_value = mock_response

        fetcher = GitHubSchemaFetcher()

        with pytest.raises(RuntimeError) as exc_info:
            fetcher.fetch_latest_release()

        assert "tag_name" in str(exc_info.value).lower()


class TestFetchFileContentWithRef:
    """Tests for fetch_file_content() with custom ref parameter."""

    @patch("declarative_configuration_sync.github_fetcher.requests.get")
    def test_fetch_file_content_accepts_ref_parameter(self, mock_get: Mock) -> None:
        """Test fetch_file_content() accepts ref parameter and uses it in API calls."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "file content"
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        fetcher = GitHubSchemaFetcher()
        content = fetcher.fetch_file_content("schema/test.yaml", ref="v0.1.0")

        assert content == "file content"
        # Verify ref parameter was passed in API call
        call_args = mock_get.call_args
        assert call_args[1]["params"]["ref"] == "v0.1.0"

    @patch("declarative_configuration_sync.github_fetcher.requests.get")
    def test_fetch_file_content_defaults_to_main_ref(self, mock_get: Mock) -> None:
        """Test fetch_file_content() defaults to main if no ref specified."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "file content"
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        fetcher = GitHubSchemaFetcher()
        fetcher.fetch_file_content("schema/test.yaml")

        # Verify default ref is main
        call_args = mock_get.call_args
        assert call_args[1]["params"]["ref"] == "main"
