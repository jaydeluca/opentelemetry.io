"""Tests for YAML schema parser."""

from pathlib import Path

import pytest

from declarative_configuration_sync.schema_parser import SchemaParser
from declarative_configuration_sync.type_defs import (
    LanguageImplementation,
    SchemaType,
)


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
        # Truly malformed YAML: unmatched bracket
        yaml_file.write_text("key: [value1, value2\nmissing: bracket")

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


class TestParseLanguageStatus:
    """Tests for SchemaParser.parse_language_status() method."""

    @pytest.fixture
    def sample_schema(self) -> dict:
        """Load sample_schema.yaml for testing."""
        fixture_path = (
            Path(__file__).parent / "fixtures" / "sample_schema.yaml"
        )
        parser = SchemaParser()
        return parser.parse_file(fixture_path)

    def test_extract_all_languages(self, sample_schema: dict) -> None:
        """Extract all language implementations from sample schema."""
        parser = SchemaParser()
        implementations = parser.parse_language_status(sample_schema)

        # Sample has cpp and java
        languages = {impl["language"] for impl in implementations}
        assert "cpp" in languages
        assert "java" in languages

    def test_language_implementation_structure(self, sample_schema: dict) -> None:
        """Validate LanguageImplementation TypedDict structure."""
        parser = SchemaParser()
        implementations = parser.parse_language_status(sample_schema)

        cpp_impls = [impl for impl in implementations if impl["language"] == "cpp"]
        assert len(cpp_impls) > 0

        # Check required fields
        impl = cpp_impls[0]
        assert impl["language"] == "cpp"
        assert impl["file_format"] == "1.0.0-rc.2"
        assert "type_name" in impl
        assert "status" in impl

    def test_extract_nested_property_status(self, sample_schema: dict) -> None:
        """Extract nested property status correctly."""
        parser = SchemaParser()
        implementations = parser.parse_language_status(sample_schema)

        # Find cpp OpenTelemetryConfiguration
        cpp_otel_config = [
            impl for impl in implementations
            if impl["language"] == "cpp" and impl["type_name"] == "OpenTelemetryConfiguration"
        ][0]

        # Should have properties
        assert "properties" in cpp_otel_config
        props = cpp_otel_config["properties"]
        assert len(props) > 0

        # Check PropertyStatus structure
        file_format_prop = [p for p in props if p["name"] == "file_format"][0]
        assert file_format_prop["status"] == "supported"

    def test_default_unknown_status(self, tmp_path: Path) -> None:
        """Use default 'unknown' status for missing status fields."""
        yaml_file = tmp_path / "minimal.yaml"
        yaml_file.write_text("""
languages:
  python:
    file_format: "1.0.0"
    types:
      - name: "TestType"
        # Missing status field
""")

        parser = SchemaParser()
        schema = parser.parse_file(yaml_file)
        implementations = parser.parse_language_status(schema)

        assert len(implementations) == 1
        assert implementations[0]["status"] == "unknown"

    def test_missing_languages_section(self) -> None:
        """Raise ValueError when 'languages' section missing."""
        parser = SchemaParser()
        invalid_schema = {"types": []}

        with pytest.raises(ValueError) as exc_info:
            parser.parse_language_status(invalid_schema)

        assert "languages" in str(exc_info.value)

    def test_skip_language_without_types(self, tmp_path: Path) -> None:
        """Skip languages that have no 'types' section."""
        yaml_file = tmp_path / "no_types.yaml"
        yaml_file.write_text("""
languages:
  python:
    file_format: "1.0.0"
    # No types section
  java:
    file_format: "1.0.0"
    types:
      - name: "ValidType"
        status: "supported"
""")

        parser = SchemaParser()
        schema = parser.parse_file(yaml_file)
        implementations = parser.parse_language_status(schema)

        # Only java should be included
        languages = {impl["language"] for impl in implementations}
        assert "python" not in languages
        assert "java" in languages


class TestParseSchemaTypes:
    """Tests for SchemaParser.parse_schema_types() method."""

    @pytest.fixture
    def sample_schema(self) -> dict:
        """Load sample_schema.yaml for testing."""
        fixture_path = (
            Path(__file__).parent / "fixtures" / "sample_schema.yaml"
        )
        parser = SchemaParser()
        return parser.parse_file(fixture_path)

    def test_extract_type_definitions(self, sample_schema: dict) -> None:
        """Extract all type definitions from schema."""
        parser = SchemaParser()
        types = parser.parse_schema_types(sample_schema)

        type_names = {t["name"] for t in types}
        assert "OpenTelemetryConfiguration" in type_names
        assert "Resource" in type_names

    def test_schema_type_structure(self, sample_schema: dict) -> None:
        """Validate SchemaType TypedDict structure."""
        parser = SchemaParser()
        types = parser.parse_schema_types(sample_schema)

        otel_config = [t for t in types if t["name"] == "OpenTelemetryConfiguration"][0]

        # Required field
        assert otel_config["name"] == "OpenTelemetryConfiguration"

        # Optional fields
        assert "description" in otel_config
        assert otel_config["description"] == "Root configuration object"

        assert "properties" in otel_config
        assert "file_format" in otel_config["properties"]

    def test_handle_optional_fields(self, tmp_path: Path) -> None:
        """Handle missing optional description and properties."""
        yaml_file = tmp_path / "minimal.yaml"
        yaml_file.write_text("""
types:
  - name: "MinimalType"
""")

        parser = SchemaParser()
        schema = parser.parse_file(yaml_file)
        types = parser.parse_schema_types(schema)

        assert len(types) == 1
        assert types[0]["name"] == "MinimalType"
        # Optional fields should not be present
        assert "description" not in types[0]
        assert "properties" not in types[0]

    def test_missing_types_section(self) -> None:
        """Raise ValueError when 'types' section missing."""
        parser = SchemaParser()
        invalid_schema = {"languages": {}}

        with pytest.raises(ValueError) as exc_info:
            parser.parse_schema_types(invalid_schema)

        assert "types" in str(exc_info.value)
