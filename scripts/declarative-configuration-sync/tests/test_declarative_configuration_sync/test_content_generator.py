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


class TestLanguageStatusTable:
    """Test language status table generation."""

    def test_generate_language_status_table_creates_complete_table(self):
        """Language status table should have header, format, and rows."""
        generator = ContentGenerator()
        implementations = [
            LanguageImplementation(
                language="cpp",
                file_format="1.0.0-rc.2",
                type_name="TypeB",
                status="supported",
            ),
            LanguageImplementation(
                language="cpp",
                file_format="1.0.0-rc.2",
                type_name="TypeA",
                status="not_implemented",
            ),
        ]
        result = generator.generate_language_status_table(implementations, "cpp")

        # Should have language header with anchor
        assert "### cpp {#cpp}" in result
        # Should have file format
        assert "Latest supported file format: `1.0.0-rc.2`" in result
        # Should have table header
        assert "| Type | Status | Notes | Support Status Details |" in result
        assert "|---|---|---|---|" in result
        # Should have rows sorted by type name
        lines = result.split("\n")
        type_a_line = next(i for i, line in enumerate(lines) if "TypeA" in line)
        type_b_line = next(i for i, line in enumerate(lines) if "TypeB" in line)
        assert type_a_line < type_b_line, "Types should be sorted alphabetically"

    def test_generate_language_status_table_empty_list(self):
        """Empty implementations list should return empty string."""
        generator = ContentGenerator()
        result = generator.generate_language_status_table([], "cpp")
        assert result == ""


class TestLanguageStatusAccordion:
    """Test language status accordion generation."""

    def test_generate_language_status_accordion_wraps_tables(self):
        """Accordion should wrap multiple language tables in Hugo shortcode."""
        generator = ContentGenerator()
        implementations_by_language = {
            "java": [
                LanguageImplementation(
                    language="java",
                    file_format="1.0.0-rc.1",
                    type_name="TestType",
                    status="supported",
                )
            ],
            "cpp": [
                LanguageImplementation(
                    language="cpp",
                    file_format="1.0.0-rc.2",
                    type_name="TestType",
                    status="supported",
                )
            ],
        }
        result = generator.generate_language_status_accordion(implementations_by_language)

        # Should have Hugo shortcode
        assert "{{< sdk-lang-status-accordion >}}" in result
        # Should have div wrapper
        assert '<div class="language-implementation-status-content" style="display: none;">' in result
        assert "</div>" in result
        # Should have both language sections
        assert "### cpp {#cpp}" in result
        assert "### java {#java}" in result
        # Languages should be sorted alphabetically
        lines = result.split("\n")
        cpp_line = next(i for i, line in enumerate(lines) if "### cpp" in line)
        java_line = next(i for i, line in enumerate(lines) if "### java" in line)
        assert cpp_line < java_line, "Languages should be sorted alphabetically"

    def test_accordion_format_matches_target_page(self):
        """Accordion structure should match target page exactly."""
        generator = ContentGenerator()
        implementations = {
            "cpp": [
                LanguageImplementation(
                    language="cpp",
                    file_format="1.0.0-rc.2",
                    type_name="Aggregation",
                    status="supported",
                    properties=[
                        PropertyStatus(name="default", status="supported"),
                        PropertyStatus(name="drop", status="supported"),
                    ],
                )
            ],
        }
        result = generator.generate_language_status_accordion(implementations)

        # Verify exact format from target page
        expected_lines = [
            "{{< sdk-lang-status-accordion >}}",
            "",
            '<div class="language-implementation-status-content" style="display: none;">',
            "",
            "### cpp {#cpp}",
        ]
        result_lines = result.split("\n")
        for i, expected in enumerate(expected_lines):
            assert result_lines[i] == expected, f"Line {i} should match: {expected}"
