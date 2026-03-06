"""Tests for YAML schema parser."""

from pathlib import Path

import pytest

from declarative_configuration_sync.schema_parser import SchemaParser


class TestParseFile:
    """Tests for SchemaParser.parse_file() method."""

    def test_parse_valid_yaml(self, tmp_path: Path) -> None:
        """Successfully parse valid YAML file."""
        yaml_file = tmp_path / "test.yaml"
        yaml_file.write_text("key: value\nnumber: 42")

        parser = SchemaParser()
        result = parser.parse_file(yaml_file)

        assert isinstance(result, dict)
        assert result["key"] == "value"
        assert result["number"] == 42

    def test_parse_sample_fixture(self) -> None:
        """Parse sample_schema.yaml fixture."""
        fixture_path = (
            Path(__file__).parent / "fixtures" / "sample_schema.yaml"
        )

        parser = SchemaParser()
        result = parser.parse_file(fixture_path)

        assert isinstance(result, dict)
        assert "types" in result
        assert "languages" in result

    def test_parse_file_not_found(self, tmp_path: Path) -> None:
        """Raise FileNotFoundError when file doesn't exist."""
        parser = SchemaParser()
        missing_file = tmp_path / "missing.yaml"

        with pytest.raises(FileNotFoundError) as exc_info:
            parser.parse_file(missing_file)

        assert str(missing_file) in str(exc_info.value)

    def test_parse_malformed_yaml(self, tmp_path: Path) -> None:
        """Raise ValueError on malformed YAML."""
        yaml_file = tmp_path / "bad.yaml"
        yaml_file.write_text("key: value\n  invalid indentation\n  - oops")

        parser = SchemaParser()

        with pytest.raises(ValueError) as exc_info:
            parser.parse_file(yaml_file)

        assert str(yaml_file) in str(exc_info.value)
        assert "Failed to parse YAML" in str(exc_info.value)

    def test_parse_yaml_not_dict(self, tmp_path: Path) -> None:
        """Raise ValueError when YAML is not a dict."""
        # YAML that parses to a list
        yaml_file = tmp_path / "list.yaml"
        yaml_file.write_text("- item1\n- item2\n- item3")

        parser = SchemaParser()

        with pytest.raises(ValueError) as exc_info:
            parser.parse_file(yaml_file)

        assert str(yaml_file) in str(exc_info.value)
        assert "Expected dict" in str(exc_info.value)
        assert "list" in str(exc_info.value)

    def test_parse_yaml_utf8_encoding(self, tmp_path: Path) -> None:
        """Handle UTF-8 encoded YAML files."""
        yaml_file = tmp_path / "utf8.yaml"
        yaml_file.write_text("name: José\ndescription: Configuración", encoding="utf-8")

        parser = SchemaParser()
        result = parser.parse_file(yaml_file)

        assert result["name"] == "José"
        assert result["description"] == "Configuración"
