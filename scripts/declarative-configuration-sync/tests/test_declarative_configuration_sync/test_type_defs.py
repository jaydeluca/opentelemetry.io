"""Tests for TypedDict data structures."""

from typing import get_type_hints

from declarative_configuration_sync.type_defs import (
    LanguageImplementation,
    PropertyStatus,
    SchemaType,
    SupportStatus,
)


def test_support_status_literals() -> None:
    """Verify SupportStatus accepts only valid literal values."""
    # This test verifies the type alias exists and has the expected literal values
    # mypy will catch invalid assignments at type-check time
    valid_statuses: list[SupportStatus] = [
        "supported",
        "not_implemented",
        "ignored",
        "unknown",
        "not_applicable",
    ]
    assert len(valid_statuses) == 5


def test_property_status_structure(sample_property_status: PropertyStatus) -> None:
    """Verify PropertyStatus has required fields."""
    assert sample_property_status["name"] == "file_format"
    assert sample_property_status["status"] == "supported"

    # Verify type hints exist
    hints = get_type_hints(PropertyStatus)
    assert "name" in hints
    assert "status" in hints


def test_language_implementation_required_fields(
    sample_language_implementation_no_properties: LanguageImplementation,
) -> None:
    """Verify LanguageImplementation requires all mandatory fields."""
    assert sample_language_implementation_no_properties["language"] == "go"
    assert sample_language_implementation_no_properties["file_format"] == "1.0.0-rc.1"
    assert sample_language_implementation_no_properties["type_name"] == "OpenTelemetryConfiguration"
    assert sample_language_implementation_no_properties["status"] == "not_implemented"


def test_language_implementation_optional_properties(
    sample_language_implementation: LanguageImplementation,
) -> None:
    """Verify LanguageImplementation optionally accepts properties list."""
    assert "properties" in sample_language_implementation
    properties = sample_language_implementation["properties"]
    assert len(properties) == 2
    assert properties[0]["name"] == "file_format"
    assert properties[1]["status"] == "not_implemented"


def test_schema_type_required_fields(sample_schema_type_minimal: SchemaType) -> None:
    """Verify SchemaType requires only name field."""
    assert sample_schema_type_minimal["name"] == "SimpleType"


def test_schema_type_optional_fields(sample_schema_type: SchemaType) -> None:
    """Verify SchemaType optionally accepts description and properties."""
    assert sample_schema_type["name"] == "OpenTelemetryConfiguration"
    assert "description" in sample_schema_type
    assert sample_schema_type["description"] == "Top-level configuration object"
    assert "properties" in sample_schema_type
    assert len(sample_schema_type["properties"]) == 4


def test_fixtures_match_expected_structure(
    sample_property_status: PropertyStatus,
    sample_language_implementation: LanguageImplementation,
    sample_schema_type: SchemaType,
) -> None:
    """Verify all fixtures provide valid TypedDict instances."""
    # PropertyStatus fixture
    assert isinstance(sample_property_status["name"], str)
    assert sample_property_status["status"] in [
        "supported",
        "not_implemented",
        "ignored",
        "unknown",
        "not_applicable",
    ]

    # LanguageImplementation fixture
    assert isinstance(sample_language_implementation["language"], str)
    assert isinstance(sample_language_implementation["file_format"], str)
    assert isinstance(sample_language_implementation["type_name"], str)

    # SchemaType fixture
    assert isinstance(sample_schema_type["name"], str)
    if "properties" in sample_schema_type:
        assert isinstance(sample_schema_type["properties"], list)
