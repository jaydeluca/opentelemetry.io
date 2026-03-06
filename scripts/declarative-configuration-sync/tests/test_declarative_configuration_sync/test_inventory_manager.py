"""Tests for InventoryManager class."""

import logging
from unittest.mock import Mock, patch

import pytest
import requests

from declarative_configuration_sync.inventory_manager import InventoryManager


@pytest.fixture
def mock_github_response() -> list[dict[str, str]]:
    """Fixture providing mock GitHub API response with mixed file types."""
    return [
        {"name": "logger.yaml", "path": "schema/logger.yaml", "type": "file"},
        {"name": "tracer_provider.yaml", "path": "schema/tracer_provider.yaml", "type": "file"},
        {
            "name": "meta_schema_v1.yaml",
            "path": "schema/meta_schema_v1.yaml",
            "type": "file",
        },
        {"name": "README.md", "path": "schema/README.md", "type": "file"},
        {"name": "meter_provider.yaml", "path": "schema/meter_provider.yaml", "type": "file"},
        {"name": "subdirectory", "path": "schema/subdirectory", "type": "dir"},
        {
            "name": "meta_schema_validation.yaml",
            "path": "schema/meta_schema_validation.yaml",
            "type": "file",
        },
    ]


def test_discover_schemas_fetches_from_github_api(
    mock_github_response: list[dict[str, str]]
) -> None:
    """Test that discover_schemas() fetches tree from GitHub API."""
    manager = InventoryManager(ref="main", timeout=30)

    with patch("requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_github_response
        mock_get.return_value = mock_response

        schemas = manager.discover_schemas()

        # Verify API call was made with correct parameters
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        assert call_args[0][0] == (
            "https://api.github.com/repos/open-telemetry/"
            "opentelemetry-configuration/contents/schema"
        )
        assert call_args[1]["params"] == {"ref": "main"}
        assert call_args[1]["timeout"] == 30

        # Should return schema files
        assert len(schemas) > 0


def test_discover_schemas_filters_out_meta_schema_files(
    mock_github_response: list[dict[str, str]]
) -> None:
    """Test that discover_schemas() filters out meta_schema_*.yaml files."""
    manager = InventoryManager()

    with patch("requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_github_response
        mock_get.return_value = mock_response

        schemas = manager.discover_schemas()

        # Should exclude meta_schema files
        assert "schema/meta_schema_v1.yaml" not in schemas
        assert "schema/meta_schema_validation.yaml" not in schemas

        # Should include regular schema files
        assert "schema/logger.yaml" in schemas
        assert "schema/tracer_provider.yaml" in schemas
        assert "schema/meter_provider.yaml" in schemas


def test_discover_schemas_returns_only_yaml_files(
    mock_github_response: list[dict[str, str]]
) -> None:
    """Test that discover_schemas() returns only .yaml files."""
    manager = InventoryManager()

    with patch("requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_github_response
        mock_get.return_value = mock_response

        schemas = manager.discover_schemas()

        # Should exclude non-yaml files
        assert "schema/README.md" not in schemas

        # Should exclude directories
        assert "schema/subdirectory" not in schemas

        # All returned paths should end with .yaml
        for schema in schemas:
            assert schema.endswith(".yaml")


def test_discover_schemas_returns_sorted_list(mock_github_response: list[dict[str, str]]) -> None:
    """Test that discover_schemas() returns sorted list by filename."""
    manager = InventoryManager()

    with patch("requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_github_response
        mock_get.return_value = mock_response

        schemas = manager.discover_schemas()

        # Should be sorted alphabetically
        assert schemas == sorted(schemas)

        # Verify expected order
        expected = [
            "schema/logger.yaml",
            "schema/meter_provider.yaml",
            "schema/tracer_provider.yaml",
        ]
        assert schemas == expected


def test_discover_schemas_raises_on_api_error() -> None:
    """Test that discover_schemas() raises RuntimeError on API errors."""
    manager = InventoryManager()

    with patch("requests.get") as mock_get:
        # Simulate connection error
        mock_get.side_effect = requests.exceptions.ConnectionError("Network error")

        with pytest.raises(RuntimeError, match="Failed to fetch schema list from GitHub"):
            manager.discover_schemas()


def test_discover_schemas_raises_on_http_error() -> None:
    """Test that discover_schemas() raises RuntimeError on HTTP errors."""
    manager = InventoryManager()

    with patch("requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("Not Found")
        mock_get.return_value = mock_response

        with pytest.raises(RuntimeError, match="Failed to fetch schema list from GitHub"):
            manager.discover_schemas()


def test_discover_schemas_logs_count(
    mock_github_response: list[dict[str, str]], caplog: pytest.LogCaptureFixture
) -> None:
    """Test that discover_schemas() logs count of discovered schemas."""
    manager = InventoryManager()

    with caplog.at_level(logging.INFO):
        with patch("requests.get") as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = mock_github_response
            mock_get.return_value = mock_response

            schemas = manager.discover_schemas()

            # Should log count of discovered schemas
            assert len(schemas) == 3
            assert "Discovered 3 schema files" in caplog.text
