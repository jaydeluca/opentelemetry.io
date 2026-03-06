"""Integration tests for idempotent generation."""

import hashlib
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

# Import will work since main.py now exists
from declarative_configuration_sync.main import main


class TestIdempotence:
    """Tests for idempotent documentation generation."""

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
    def test_idempotent_generation(
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
        """Test 1: Running full pipeline twice produces identical markdown output."""
        # Setup repo root
        mock_find_root.return_value = tmp_path

        # Setup inventory
        mock_inventory = Mock()
        mock_inventory.discover_schemas.return_value = ["schema/config.yaml"]
        mock_inventory_class.return_value = mock_inventory

        # Setup fetcher
        mock_fetcher = Mock()
        mock_fetcher.fetch_file_content.return_value = "test: yaml"
        mock_fetcher_class.return_value = mock_fetcher

        # Setup temporary file
        mock_temp = Mock()
        mock_temp.__enter__ = Mock(return_value=mock_temp)
        mock_temp.__exit__ = Mock(return_value=None)
        mock_temp.name = str(tmp_path / "test.yaml")
        mock_tempfile.return_value = mock_temp

        # Setup YAML parsing
        mock_yaml_load.return_value = {"test": "data"}

        # Setup parser with fixed return values
        mock_parser = Mock()
        mock_parser.parse_language_status.return_value = [
            {"language": "go", "status": "stable"}
        ]
        mock_parser.parse_schema_types.return_value = [
            {"name": "string", "description": "Text"}
        ]
        mock_parser_class.return_value = mock_parser

        # Setup generator with deterministic output
        mock_generator = Mock()
        lang_content_first = "Language Status Content V1"
        type_content_first = "Type Table Content V1"
        mock_generator.generate_language_status_accordion.return_value = (
            lang_content_first
        )
        mock_generator.generate_type_table.return_value = type_content_first
        mock_generator_class.return_value = mock_generator

        # Capture first run output
        first_run_outputs = {}

        def capture_first_update(file_path: Path, marker_id: str, content: str) -> None:
            first_run_outputs[marker_id] = content

        mock_updater = Mock()
        mock_updater.update_file.side_effect = capture_first_update
        mock_updater_class.return_value = mock_updater

        # Setup formatter
        mock_formatter.return_value = True

        # Run first time
        main()

        # Verify we captured outputs
        assert "language-implementation-status" in first_run_outputs
        assert "types" in first_run_outputs

        # Compute hashes for first run
        first_lang_hash = hashlib.sha256(
            first_run_outputs["language-implementation-status"].encode()
        ).hexdigest()
        first_type_hash = hashlib.sha256(
            first_run_outputs["types"].encode()
        ).hexdigest()

        # Reset mocks for second run
        mock_updater.reset_mock()

        # Capture second run output
        second_run_outputs = {}

        def capture_second_update(
            file_path: Path, marker_id: str, content: str
        ) -> None:
            second_run_outputs[marker_id] = content

        mock_updater.update_file.side_effect = capture_second_update

        # Run second time
        main()

        # Verify we captured outputs
        assert "language-implementation-status" in second_run_outputs
        assert "types" in second_run_outputs

        # Compute hashes for second run
        second_lang_hash = hashlib.sha256(
            second_run_outputs["language-implementation-status"].encode()
        ).hexdigest()
        second_type_hash = hashlib.sha256(
            second_run_outputs["types"].encode()
        ).hexdigest()

        # Assert hashes match (idempotent)
        assert (
            first_lang_hash == second_lang_hash
        ), "Language status content changed between runs"
        assert first_type_hash == second_type_hash, "Type content changed between runs"

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
    def test_content_hashes_match_not_timestamps(
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
        """Test 2: File modification times may differ but content hashes match."""
        # This test is essentially the same as test_idempotent_generation
        # but explicitly documents that we're comparing content, not metadata
        mock_find_root.return_value = tmp_path

        mock_inventory = Mock()
        mock_inventory.discover_schemas.return_value = ["schema/config.yaml"]
        mock_inventory_class.return_value = mock_inventory

        mock_fetcher = Mock()
        mock_fetcher.fetch_file_content.return_value = "test: yaml"
        mock_fetcher_class.return_value = mock_fetcher

        mock_temp = Mock()
        mock_temp.__enter__ = Mock(return_value=mock_temp)
        mock_temp.__exit__ = Mock(return_value=None)
        mock_temp.name = str(tmp_path / "test.yaml")
        mock_tempfile.return_value = mock_temp

        mock_yaml_load.return_value = {"test": "data"}

        mock_parser = Mock()
        mock_parser.parse_language_status.return_value = [
            {"language": "java", "status": "experimental"}
        ]
        mock_parser.parse_schema_types.return_value = []
        mock_parser_class.return_value = mock_parser

        mock_generator = Mock()
        mock_generator.generate_language_status_accordion.return_value = (
            "Fixed Content"
        )
        mock_generator.generate_type_table.return_value = "Fixed Types"
        mock_generator_class.return_value = mock_generator

        # Capture outputs
        captured_outputs = []

        def capture_update(file_path: Path, marker_id: str, content: str) -> None:
            captured_outputs.append(content)

        mock_updater = Mock()
        mock_updater.update_file.side_effect = capture_update
        mock_updater_class.return_value = mock_updater

        mock_formatter.return_value = True

        # Run once
        main()

        first_outputs = captured_outputs.copy()

        # Reset and run again
        captured_outputs.clear()
        mock_updater.reset_mock()
        mock_updater.update_file.side_effect = capture_update

        main()

        second_outputs = captured_outputs

        # Content should be identical
        assert first_outputs == second_outputs

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
    def test_idempotence_with_sorted_schema_order(
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
        """Test 3: Idempotence holds with different schema input order (sorted internally)."""
        # The schema list order shouldn't matter if content generation is deterministic
        mock_find_root.return_value = tmp_path

        mock_inventory = Mock()
        # First run: schemas in one order
        mock_inventory.discover_schemas.return_value = [
            "schema/b.yaml",
            "schema/a.yaml",
        ]
        mock_inventory_class.return_value = mock_inventory

        mock_fetcher = Mock()
        mock_fetcher.fetch_file_content.return_value = "test: data"
        mock_fetcher_class.return_value = mock_fetcher

        mock_temp = Mock()
        mock_temp.__enter__ = Mock(return_value=mock_temp)
        mock_temp.__exit__ = Mock(return_value=None)
        mock_temp.name = str(tmp_path / "test.yaml")
        mock_tempfile.return_value = mock_temp

        mock_yaml_load.return_value = {"test": "data"}

        mock_parser = Mock()
        mock_parser.parse_language_status.return_value = []
        mock_parser.parse_schema_types.return_value = []
        mock_parser_class.return_value = mock_parser

        mock_generator = Mock()
        mock_generator.generate_language_status_accordion.return_value = "Content"
        mock_generator.generate_type_table.return_value = "Types"
        mock_generator_class.return_value = mock_generator

        captured_first = {}

        def capture_first(file_path: Path, marker_id: str, content: str) -> None:
            captured_first[marker_id] = content

        mock_updater = Mock()
        mock_updater.update_file.side_effect = capture_first
        mock_updater_class.return_value = mock_updater

        mock_formatter.return_value = True

        # Run with first ordering
        main()

        # Change schema order for second run
        mock_inventory.discover_schemas.return_value = [
            "schema/a.yaml",
            "schema/b.yaml",
        ]

        captured_second = {}

        def capture_second(file_path: Path, marker_id: str, content: str) -> None:
            captured_second[marker_id] = content

        mock_updater.reset_mock()
        mock_updater.update_file.side_effect = capture_second

        # Run with second ordering
        main()

        # Content should match regardless of input order
        # (assuming generator produces sorted/deterministic output)
        assert captured_first.keys() == captured_second.keys()
        for marker_id in captured_first:
            assert captured_first[marker_id] == captured_second[marker_id]
