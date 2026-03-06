"""Integration tests for main() CLI orchestration."""

import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, Mock, call, patch

import pytest


# Import will initially have incomplete main() - tests will fail
from declarative_configuration_sync.main import main


class TestMainOrchestration:
    """Tests for main() function orchestration."""

    @patch("sys.argv", ["main", "--mode=lang-status"])
    @patch("declarative_configuration_sync.main.find_repo_root")
    @patch("logging.basicConfig")
    def test_sets_up_logging(self, mock_logging: Mock, mock_find_root: Mock) -> None:
        """Test 1: main() sets up logging with INFO level."""
        mock_find_root.side_effect = RuntimeError("Stop execution")

        with pytest.raises(SystemExit):
            main()

        # Verify logging was configured
        mock_logging.assert_called_once()
        call_kwargs = mock_logging.call_args[1]
        assert call_kwargs["level"] == 20  # logging.INFO

    @patch("sys.argv", ["main", "--mode=lang-status"])
    @patch("declarative_configuration_sync.main.run_npm_formatter")
    @patch("declarative_configuration_sync.main.InventoryManager")
    @patch("declarative_configuration_sync.main.os.chdir")
    @patch("declarative_configuration_sync.main.find_repo_root")
    def test_finds_repo_root_and_changes_directory(
        self, mock_find_root: Mock, mock_chdir: Mock, mock_inventory_class: Mock, mock_formatter: Mock, tmp_path: Path
    ) -> None:
        """Test 2: main() finds repo root and changes working directory."""
        mock_find_root.return_value = tmp_path
        mock_inventory = Mock()
        mock_inventory.discover_schemas.return_value = []
        mock_inventory_class.return_value = mock_inventory
        mock_formatter.return_value = True

        main()

        # Verify repo root was found and chdir was called
        assert mock_find_root.call_count >= 1
        mock_chdir.assert_called_once_with(tmp_path)

    @patch("sys.argv", ["main", "--mode=lang-status"])
    @patch("declarative_configuration_sync.main.run_npm_formatter")
    @patch("declarative_configuration_sync.main.MarkerUpdater")
    @patch("declarative_configuration_sync.main.ContentGenerator")
    @patch("declarative_configuration_sync.main.SchemaParser")
    @patch("declarative_configuration_sync.main.InventoryManager")
    @patch("declarative_configuration_sync.main.GitHubSchemaFetcher")
    @patch("declarative_configuration_sync.main.os.chdir")
    @patch("declarative_configuration_sync.main.find_repo_root")
    def test_creates_github_clients(
        self,
        mock_find_root: Mock,
        mock_chdir: Mock,
        mock_fetcher_class: Mock,
        mock_inventory_class: Mock,
        mock_parser_class: Mock,
        mock_generator_class: Mock,
        mock_updater_class: Mock,
        mock_formatter: Mock,
        tmp_path: Path,
    ) -> None:
        """Test 3: main() creates GitHubSchemaFetcher and InventoryManager."""
        mock_find_root.return_value = tmp_path
        mock_inventory = Mock()
        mock_inventory.discover_schemas.return_value = []
        mock_inventory_class.return_value = mock_inventory
        mock_formatter.return_value = True

        main()

        # Verify GitHub clients were instantiated
        mock_fetcher_class.assert_called_once()
        mock_inventory_class.assert_called_once()

    @patch("sys.argv", ["main", "--mode=lang-status"])
    @patch("declarative_configuration_sync.main.run_npm_formatter")
    @patch("declarative_configuration_sync.main.MarkerUpdater")
    @patch("declarative_configuration_sync.main.ContentGenerator")
    @patch("declarative_configuration_sync.main.SchemaParser")
    @patch("declarative_configuration_sync.main.InventoryManager")
    @patch("declarative_configuration_sync.main.GitHubSchemaFetcher")
    @patch("declarative_configuration_sync.main.os.chdir")
    @patch("declarative_configuration_sync.main.find_repo_root")
    def test_discovers_schemas(
        self,
        mock_find_root: Mock,
        mock_chdir: Mock,
        mock_fetcher_class: Mock,
        mock_inventory_class: Mock,
        mock_parser_class: Mock,
        mock_generator_class: Mock,
        mock_updater_class: Mock,
        mock_formatter: Mock,
        tmp_path: Path,
    ) -> None:
        """Test 4: main() discovers schemas via InventoryManager."""
        mock_find_root.return_value = tmp_path
        mock_inventory = Mock()
        mock_inventory.discover_schemas.return_value = []
        mock_inventory_class.return_value = mock_inventory
        mock_formatter.return_value = True

        main()

        # Verify discover_schemas was called
        mock_inventory.discover_schemas.assert_called_once()

    @patch("sys.argv", ["main", "--mode=lang-status"])
    @patch("builtins.open", new_callable=MagicMock)
    @patch("declarative_configuration_sync.main.yaml.safe_load")
    @patch("declarative_configuration_sync.main.tempfile.NamedTemporaryFile")
    @patch("declarative_configuration_sync.main.run_npm_formatter")
    @patch("declarative_configuration_sync.main.MarkerUpdater")
    @patch("declarative_configuration_sync.main.ContentGenerator")
    @patch("declarative_configuration_sync.main.SchemaParser")
    @patch("declarative_configuration_sync.main.InventoryManager")
    @patch("declarative_configuration_sync.main.GitHubSchemaFetcher")
    @patch("declarative_configuration_sync.main.os.chdir")
    @patch("declarative_configuration_sync.main.find_repo_root")
    def test_fetches_schema_files(
        self,
        mock_find_root: Mock,
        mock_chdir: Mock,
        mock_fetcher_class: Mock,
        mock_inventory_class: Mock,
        mock_parser_class: Mock,
        mock_generator_class: Mock,
        mock_updater_class: Mock,
        mock_formatter: Mock,
        mock_tempfile: Mock,
        mock_yaml_load: Mock,
        mock_open: Mock,
        tmp_path: Path,
    ) -> None:
        """Test 5: main() fetches each schema file via GitHubSchemaFetcher."""
        mock_find_root.return_value = tmp_path
        mock_inventory = Mock()
        mock_inventory.discover_schemas.return_value = ["schema/config.yaml"]
        mock_inventory_class.return_value = mock_inventory

        mock_fetcher = Mock()
        mock_fetcher.fetch_file_content.return_value = "yaml: content"
        mock_fetcher_class.return_value = mock_fetcher

        # Mock temporary file
        mock_temp = Mock()
        mock_temp.__enter__ = Mock(return_value=mock_temp)
        mock_temp.__exit__ = Mock(return_value=None)
        mock_temp.name = "/tmp/test.yaml"
        mock_tempfile.return_value = mock_temp

        # Mock YAML parsing
        mock_yaml_load.return_value = {}

        # Mock parser/generator
        mock_parser = Mock()
        mock_parser.parse_language_status.return_value = []
        mock_parser.parse_schema_types.return_value = []
        mock_parser_class.return_value = mock_parser

        mock_generator = Mock()
        mock_generator.generate_language_status_accordion.return_value = "content"
        mock_generator.generate_type_table.return_value = "content"
        mock_generator_class.return_value = mock_generator

        mock_updater = Mock()
        mock_updater_class.return_value = mock_updater

        mock_formatter.return_value = True

        main()

        # Verify schema was fetched
        mock_fetcher.fetch_file_content.assert_called_once_with("schema/config.yaml")

    @patch("sys.argv", ["main", "--mode=lang-status"])
    @patch("builtins.open", new_callable=MagicMock)
    @patch("declarative_configuration_sync.main.yaml.safe_load")
    @patch("declarative_configuration_sync.main.Path.unlink")
    @patch("declarative_configuration_sync.main.tempfile.NamedTemporaryFile")
    @patch("declarative_configuration_sync.main.run_npm_formatter")
    @patch("declarative_configuration_sync.main.MarkerUpdater")
    @patch("declarative_configuration_sync.main.ContentGenerator")
    @patch("declarative_configuration_sync.main.SchemaParser")
    @patch("declarative_configuration_sync.main.InventoryManager")
    @patch("declarative_configuration_sync.main.GitHubSchemaFetcher")
    @patch("declarative_configuration_sync.main.os.chdir")
    @patch("declarative_configuration_sync.main.find_repo_root")
    def test_writes_content_to_temp_files(
        self,
        mock_find_root: Mock,
        mock_chdir: Mock,
        mock_fetcher_class: Mock,
        mock_inventory_class: Mock,
        mock_parser_class: Mock,
        mock_generator_class: Mock,
        mock_updater_class: Mock,
        mock_formatter: Mock,
        mock_tempfile: Mock,
        mock_unlink: Mock,
        mock_yaml_load: Mock,
        mock_open: Mock,
        tmp_path: Path,
    ) -> None:
        """Test 6: main() writes fetched content to temporary files for parsing."""
        mock_find_root.return_value = tmp_path
        mock_inventory = Mock()
        mock_inventory.discover_schemas.return_value = ["schema/config.yaml"]
        mock_inventory_class.return_value = mock_inventory

        mock_fetcher = Mock()
        mock_fetcher.fetch_file_content.return_value = "yaml: content"
        mock_fetcher_class.return_value = mock_fetcher

        # Mock temporary file
        mock_temp = Mock()
        mock_temp.write = Mock()
        mock_temp.name = "/tmp/test.yaml"
        mock_temp.__enter__ = Mock(return_value=mock_temp)
        mock_temp.__exit__ = Mock(return_value=None)
        mock_tempfile.return_value = mock_temp

        # Mock YAML parsing
        mock_yaml_load.return_value = {}

        # Mock parser/generator
        mock_parser = Mock()
        mock_parser.parse_language_status.return_value = []
        mock_parser.parse_schema_types.return_value = []
        mock_parser_class.return_value = mock_parser

        mock_generator = Mock()
        mock_generator.generate_language_status_accordion.return_value = "content"
        mock_generator.generate_type_table.return_value = "content"
        mock_generator_class.return_value = mock_generator

        mock_updater = Mock()
        mock_updater_class.return_value = mock_updater

        mock_formatter.return_value = True

        main()

        # Verify content was written to temp file
        mock_temp.write.assert_called_once_with("yaml: content")

    @patch("sys.argv", ["main", "--mode=lang-status"])
    @patch("builtins.open", new_callable=MagicMock)
    @patch("declarative_configuration_sync.main.yaml.safe_load")
    @patch("declarative_configuration_sync.main.tempfile.NamedTemporaryFile")
    @patch("declarative_configuration_sync.main.run_npm_formatter")
    @patch("declarative_configuration_sync.main.MarkerUpdater")
    @patch("declarative_configuration_sync.main.ContentGenerator")
    @patch("declarative_configuration_sync.main.SchemaParser")
    @patch("declarative_configuration_sync.main.InventoryManager")
    @patch("declarative_configuration_sync.main.GitHubSchemaFetcher")
    @patch("declarative_configuration_sync.main.os.chdir")
    @patch("declarative_configuration_sync.main.find_repo_root")
    def test_generates_documentation(
        self,
        mock_find_root: Mock,
        mock_chdir: Mock,
        mock_fetcher_class: Mock,
        mock_inventory_class: Mock,
        mock_parser_class: Mock,
        mock_generator_class: Mock,
        mock_updater_class: Mock,
        mock_formatter: Mock,
        mock_tempfile: Mock,
        mock_yaml_load: Mock,
        mock_open: Mock,
        tmp_path: Path,
    ) -> None:
        """Test 7: main() generates both language status and type documentation."""
        mock_find_root.return_value = tmp_path
        mock_inventory = Mock()
        mock_inventory.discover_schemas.return_value = ["schema/config.yaml"]
        mock_inventory_class.return_value = mock_inventory

        mock_fetcher = Mock()
        mock_fetcher.fetch_file_content.return_value = "yaml: content"
        mock_fetcher_class.return_value = mock_fetcher

        # Mock temporary file
        mock_temp = Mock()
        mock_temp.__enter__ = Mock(return_value=mock_temp)
        mock_temp.__exit__ = Mock(return_value=None)
        mock_temp.name = "/tmp/test.yaml"
        mock_tempfile.return_value = mock_temp

        # Mock YAML parsing
        mock_yaml_load.return_value = {}

        # Mock parser
        mock_parser = Mock()
        mock_implementations = [{"language": "go"}]
        mock_types = [Mock()]
        mock_parser.parse_language_status.return_value = mock_implementations
        mock_parser.parse_schema_types.return_value = mock_types
        mock_parser_class.return_value = mock_parser

        # Mock generator
        mock_generator = Mock()
        mock_generator.generate_language_status_accordion.return_value = "lang content"
        mock_generator.generate_type_table.return_value = "type content"
        mock_generator_class.return_value = mock_generator

        mock_updater = Mock()
        mock_updater_class.return_value = mock_updater

        mock_formatter.return_value = True

        main()

        # Verify both generation methods were called
        # Should be called with implementations grouped by language
        mock_generator.generate_language_status_accordion.assert_called_once()
        mock_generator.generate_type_table.assert_called_once_with(mock_types)

    @patch("sys.argv", ["main", "--mode=lang-status"])
    @patch("builtins.open", new_callable=MagicMock)
    @patch("declarative_configuration_sync.main.yaml.safe_load")
    @patch("declarative_configuration_sync.main.tempfile.NamedTemporaryFile")
    @patch("declarative_configuration_sync.main.run_npm_formatter")
    @patch("declarative_configuration_sync.main.MarkerUpdater")
    @patch("declarative_configuration_sync.main.ContentGenerator")
    @patch("declarative_configuration_sync.main.SchemaParser")
    @patch("declarative_configuration_sync.main.InventoryManager")
    @patch("declarative_configuration_sync.main.GitHubSchemaFetcher")
    @patch("declarative_configuration_sync.main.os.chdir")
    @patch("declarative_configuration_sync.main.find_repo_root")
    def test_updates_target_markdown_files(
        self,
        mock_find_root: Mock,
        mock_chdir: Mock,
        mock_fetcher_class: Mock,
        mock_inventory_class: Mock,
        mock_parser_class: Mock,
        mock_generator_class: Mock,
        mock_updater_class: Mock,
        mock_formatter: Mock,
        mock_tempfile: Mock,
        mock_yaml_load: Mock,
        mock_open: Mock,
        tmp_path: Path,
    ) -> None:
        """Test 8: main() updates target markdown files with marker injection."""
        mock_find_root.return_value = tmp_path
        mock_inventory = Mock()
        mock_inventory.discover_schemas.return_value = ["schema/config.yaml"]
        mock_inventory_class.return_value = mock_inventory

        mock_fetcher = Mock()
        mock_fetcher.fetch_file_content.return_value = "yaml: content"
        mock_fetcher_class.return_value = mock_fetcher

        # Mock temporary file
        mock_temp = Mock()
        mock_temp.__enter__ = Mock(return_value=mock_temp)
        mock_temp.__exit__ = Mock(return_value=None)
        mock_temp.name = "/tmp/test.yaml"
        mock_tempfile.return_value = mock_temp

        # Mock YAML parsing
        mock_yaml_load.return_value = {}

        # Mock parser/generator
        mock_parser = Mock()
        mock_parser.parse_language_status.return_value = []
        mock_parser.parse_schema_types.return_value = []
        mock_parser_class.return_value = mock_parser

        mock_generator = Mock()
        mock_generator.generate_language_status_accordion.return_value = "lang content"
        mock_generator.generate_type_table.return_value = "type content"
        mock_generator_class.return_value = mock_generator

        mock_updater = Mock()
        mock_updater_class.return_value = mock_updater

        mock_formatter.return_value = True

        main()

        # Verify both target files were updated
        assert mock_updater.update_file.call_count == 2

        # Check the calls
        calls = mock_updater.update_file.call_args_list

        # First call should be language-implementation-status
        assert "language-implementation-status.md" in str(calls[0][0][0])
        assert calls[0][0][1] == "language-implementation-status"
        assert calls[0][0][2] == "lang content"

        # Second call should be types
        assert "types.md" in str(calls[1][0][0])
        assert calls[1][0][1] == "types"
        assert calls[1][0][2] == "type content"

    @patch("sys.argv", ["main", "--mode=lang-status"])
    @patch("builtins.open", new_callable=MagicMock)
    @patch("declarative_configuration_sync.main.yaml.safe_load")
    @patch("declarative_configuration_sync.main.tempfile.NamedTemporaryFile")
    @patch("declarative_configuration_sync.main.run_npm_formatter")
    @patch("declarative_configuration_sync.main.MarkerUpdater")
    @patch("declarative_configuration_sync.main.ContentGenerator")
    @patch("declarative_configuration_sync.main.SchemaParser")
    @patch("declarative_configuration_sync.main.InventoryManager")
    @patch("declarative_configuration_sync.main.GitHubSchemaFetcher")
    @patch("declarative_configuration_sync.main.os.chdir")
    @patch("declarative_configuration_sync.main.find_repo_root")
    def test_calls_npm_formatter(
        self,
        mock_find_root: Mock,
        mock_chdir: Mock,
        mock_fetcher_class: Mock,
        mock_inventory_class: Mock,
        mock_parser_class: Mock,
        mock_generator_class: Mock,
        mock_updater_class: Mock,
        mock_formatter: Mock,
        mock_tempfile: Mock,
        mock_yaml_load: Mock,
        mock_open: Mock,
        tmp_path: Path,
    ) -> None:
        """Test 9: main() calls run_npm_formatter() after content generation."""
        mock_find_root.return_value = tmp_path
        mock_inventory = Mock()
        mock_inventory.discover_schemas.return_value = []
        mock_inventory_class.return_value = mock_inventory
        mock_formatter.return_value = True

        main()

        # Verify formatter was called with repo root
        mock_formatter.assert_called_once_with(tmp_path)

    @patch("sys.argv", ["main", "--mode=lang-status"])
    @patch("declarative_configuration_sync.main.run_npm_formatter")
    @patch("declarative_configuration_sync.main.MarkerUpdater")
    @patch("declarative_configuration_sync.main.ContentGenerator")
    @patch("declarative_configuration_sync.main.SchemaParser")
    @patch("declarative_configuration_sync.main.InventoryManager")
    @patch("declarative_configuration_sync.main.GitHubSchemaFetcher")
    @patch("declarative_configuration_sync.main.os.chdir")
    @patch("declarative_configuration_sync.main.find_repo_root")
    def test_exits_with_zero_on_success(
        self,
        mock_find_root: Mock,
        mock_chdir: Mock,
        mock_fetcher_class: Mock,
        mock_inventory_class: Mock,
        mock_parser_class: Mock,
        mock_generator_class: Mock,
        mock_updater_class: Mock,
        mock_formatter: Mock,
        tmp_path: Path,
    ) -> None:
        """Test 10: main() exits with code 0 on success."""
        mock_find_root.return_value = tmp_path
        mock_inventory = Mock()
        mock_inventory.discover_schemas.return_value = []
        mock_inventory_class.return_value = mock_inventory
        mock_formatter.return_value = True

        # Should not raise SystemExit
        main()

    @patch("sys.argv", ["main", "--mode=lang-status"])
    @patch("declarative_configuration_sync.main.find_repo_root")
    def test_exits_with_one_on_repo_root_error(
        self, mock_find_root: Mock
    ) -> None:
        """Test 11: main() exits with code 1 on critical errors."""
        mock_find_root.side_effect = RuntimeError("Not in repo")

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 1

    @patch("sys.argv", ["main", "--mode=lang-status"])
    @patch("declarative_configuration_sync.main.os.chdir")
    @patch("declarative_configuration_sync.main.find_repo_root")
    @patch("declarative_configuration_sync.main.InventoryManager")
    def test_exits_with_one_on_discovery_error(
        self, mock_inventory_class: Mock, mock_find_root: Mock, mock_chdir: Mock, tmp_path: Path
    ) -> None:
        """Test main() exits with code 1 on schema discovery error."""
        mock_find_root.return_value = tmp_path
        mock_inventory = Mock()
        mock_inventory.discover_schemas.side_effect = RuntimeError("API error")
        mock_inventory_class.return_value = mock_inventory

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 1


class TestModeArgumentParsing:
    """Tests for --mode argument parsing."""

    @patch("sys.argv", ["main", "--mode=lang-status"])
    @patch("declarative_configuration_sync.main.run_npm_formatter")
    @patch("declarative_configuration_sync.main.InventoryManager")
    @patch("declarative_configuration_sync.main.os.chdir")
    @patch("declarative_configuration_sync.main.find_repo_root")
    def test_mode_lang_status_parses_successfully(
        self, mock_find_root: Mock, mock_chdir: Mock, mock_inventory_class: Mock, mock_formatter: Mock, tmp_path: Path
    ) -> None:
        """Test 1: main() with --mode=lang-status parses successfully."""
        mock_find_root.return_value = tmp_path
        mock_inventory = Mock()
        mock_inventory.discover_schemas.return_value = []
        mock_inventory_class.return_value = mock_inventory
        mock_formatter.return_value = True

        # Should not raise SystemExit
        main()

    @patch("sys.argv", ["main", "--mode=types"])
    @patch("declarative_configuration_sync.main.run_npm_formatter")
    @patch("declarative_configuration_sync.main.InventoryManager")
    @patch("declarative_configuration_sync.main.os.chdir")
    @patch("declarative_configuration_sync.main.find_repo_root")
    def test_mode_types_parses_successfully(
        self, mock_find_root: Mock, mock_chdir: Mock, mock_inventory_class: Mock, mock_formatter: Mock, tmp_path: Path
    ) -> None:
        """Test 2: main() with --mode=types parses successfully."""
        mock_find_root.return_value = tmp_path
        mock_inventory = Mock()
        mock_inventory.discover_schemas.return_value = []
        mock_inventory_class.return_value = mock_inventory
        mock_formatter.return_value = True

        # Should not raise SystemExit
        main()

    @patch("sys.argv", ["main"])
    def test_missing_mode_flag_exits_with_error(self) -> None:
        """Test 3: main() without --mode flag exits with error."""
        with pytest.raises(SystemExit) as exc_info:
            main()

        # argparse exits with code 2 for invalid arguments
        assert exc_info.value.code == 2

    @patch("sys.argv", ["main", "--mode=invalid"])
    def test_invalid_mode_value_exits_with_error(self) -> None:
        """Test 4: main() with invalid mode value exits with error."""
        with pytest.raises(SystemExit) as exc_info:
            main()

        # argparse exits with code 2 for invalid argument values
        assert exc_info.value.code == 2
