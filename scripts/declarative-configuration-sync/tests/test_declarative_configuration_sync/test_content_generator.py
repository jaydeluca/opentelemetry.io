"""Tests for ContentGenerator module."""

import pytest

from declarative_configuration_sync.content_generator import ContentGenerator
from declarative_configuration_sync.type_defs import (
    LanguageImplementation,
    PropertyStatus,
)


class TestMarkdownEscaping:
    """Test markdown table content escaping."""

    def test_escape_pipe_characters(self):
        """Pipe characters should be escaped to prevent table corruption."""
        generator = ContentGenerator()
        result = generator.escape_markdown_table_content("foo|bar|baz")
        assert result == "foo\\|bar\\|baz"

    def test_escape_no_pipes(self):
        """Text without pipes should pass through unchanged."""
        generator = ContentGenerator()
        result = generator.escape_markdown_table_content("normal text")
        assert result == "normal text"


class TestPropertyStatusCell:
    """Test property status cell generation."""

    def test_generate_property_list_with_br_tags(self):
        """Property list should use HTML <br> tags for line breaks."""
        generator = ContentGenerator()
        properties = [
            PropertyStatus(name="prop1", status="supported"),
            PropertyStatus(name="prop2", status="not_implemented"),
        ]
        result = generator.generate_property_status_cell(properties)
        assert "• `prop1`: supported<br>• `prop2`: not_implemented" == result

    def test_generate_property_list_escapes_pipe_in_names(self):
        """Property names with pipes should be escaped."""
        generator = ContentGenerator()
        properties = [PropertyStatus(name="foo|bar", status="supported")]
        result = generator.generate_property_status_cell(properties)
        assert "foo\\|bar" in result

    def test_empty_property_list_returns_empty_string(self):
        """Empty property list should return empty string."""
        generator = ContentGenerator()
        result = generator.generate_property_status_cell([])
        assert result == ""


class TestTableRowGeneration:
    """Test table row generation."""

    def test_generate_table_row_with_properties(
        self, sample_language_implementation: LanguageImplementation
    ):
        """Table row should include type link, status, and property details."""
        generator = ContentGenerator()
        result = generator.generate_table_row(sample_language_implementation)

        # Should have type link with anchor
        assert "[`OpenTelemetryConfiguration`](../types#opentelemetryconfiguration)" in result
        # Should have status
        assert "supported" in result
        # Should have properties with <br> tags
        assert "file_format" in result
        assert "<br>" in result
        # Should be a valid markdown row
        assert result.startswith("| ")
        assert result.endswith("|")

    def test_generate_table_row_without_properties(
        self, sample_language_implementation_no_properties: LanguageImplementation
    ):
        """Table row without properties should have empty details cell."""
        generator = ContentGenerator()
        result = generator.generate_table_row(sample_language_implementation_no_properties)

        # Should have type link
        assert "[`OpenTelemetryConfiguration`](../types#opentelemetryconfiguration)" in result
        # Should have status
        assert "not_implemented" in result
        # Should have spaces for alignment in empty details column
        assert "|  |" in result or result.endswith("  |")

    def test_type_name_uses_lowercase_anchor(self):
        """Type links should use lowercase anchors."""
        generator = ContentGenerator()
        impl = LanguageImplementation(
            language="cpp",
            file_format="1.0.0-rc.2",
            type_name="MixedCaseType",
            status="supported",
        )
        result = generator.generate_table_row(impl)
        assert "#mixedcasetype" in result
        assert "#MixedCaseType" not in result
