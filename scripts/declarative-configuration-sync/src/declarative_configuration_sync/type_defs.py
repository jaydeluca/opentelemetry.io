"""Shared type definitions for declarative-configuration-sync.

This module contains TypedDict definitions for schema data structures
parsed from opentelemetry-configuration repository YAML files.
"""

from typing import Literal, NotRequired, TypedDict

# Support status values observed in target markdown page
SupportStatus = Literal[
    "supported",
    "not_implemented",
    "ignored",
    "unknown",
    "not_applicable",
]


class PropertyStatus(TypedDict):
    """Status of a single property within a type for a specific language."""

    name: str
    status: SupportStatus


class LanguageImplementation(TypedDict):
    """Language-specific implementation status for a configuration type."""

    language: str  # e.g., "cpp", "java", "go"
    file_format: str  # e.g., "1.0.0-rc.2"
    type_name: str  # e.g., "OpenTelemetryConfiguration"
    status: SupportStatus
    properties: NotRequired[list[PropertyStatus]]  # Nested property status


class SchemaType(TypedDict):
    """Configuration type definition from schema."""

    name: str
    description: NotRequired[str]
    properties: NotRequired[list[str]]  # List of property names
