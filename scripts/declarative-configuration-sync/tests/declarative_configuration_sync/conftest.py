"""Shared pytest fixtures for declarative-configuration-sync tests."""

import pytest

from declarative_configuration_sync.type_defs import (
    LanguageImplementation,
    PropertyStatus,
    SchemaType,
)


@pytest.fixture
def sample_property_status() -> PropertyStatus:
    """Provide a sample PropertyStatus instance."""
    return PropertyStatus(name="file_format", status="supported")


@pytest.fixture
def sample_language_implementation() -> LanguageImplementation:
    """Provide a sample LanguageImplementation instance with properties."""
    return LanguageImplementation(
        language="cpp",
        file_format="1.0.0-rc.2",
        type_name="OpenTelemetryConfiguration",
        status="supported",
        properties=[
            PropertyStatus(name="file_format", status="supported"),
            PropertyStatus(name="disabled", status="not_implemented"),
        ],
    )


@pytest.fixture
def sample_language_implementation_no_properties() -> LanguageImplementation:
    """Provide a sample LanguageImplementation instance without properties."""
    return LanguageImplementation(
        language="go",
        file_format="1.0.0-rc.1",
        type_name="OpenTelemetryConfiguration",
        status="not_implemented",
    )


@pytest.fixture
def sample_schema_type() -> SchemaType:
    """Provide a sample SchemaType instance."""
    return SchemaType(
        name="OpenTelemetryConfiguration",
        description="Top-level configuration object",
        properties=["file_format", "disabled", "resource", "attribute_limits"],
    )


@pytest.fixture
def sample_schema_type_minimal() -> SchemaType:
    """Provide a minimal SchemaType instance."""
    return SchemaType(name="SimpleType")
