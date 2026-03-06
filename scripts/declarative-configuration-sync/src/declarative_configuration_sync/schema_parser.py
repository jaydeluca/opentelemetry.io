"""YAML schema parser for OpenTelemetry configuration schemas."""

import yaml
from pathlib import Path
from typing import Any

from declarative_configuration_sync.type_defs import (
    LanguageImplementation,
    PropertyStatus,
    SchemaType,
    SupportStatus,
)


class SchemaParser:
    """Parse YAML schema files from opentelemetry-configuration repository."""

    def parse_file(self, file_path: Path) -> dict[str, Any]:
        """Parse YAML schema file with safety and error context.

        Args:
            file_path: Path to YAML schema file

        Returns:
            Parsed schema data as dict

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If YAML is malformed or not a dict
        """
        try:
            with file_path.open('r', encoding='utf-8') as f:
                data = yaml.safe_load(f)

            if not isinstance(data, dict):
                raise ValueError(
                    f"Expected dict from {file_path}, got {type(data).__name__}"
                )

            return data

        except yaml.YAMLError as e:
            raise ValueError(
                f"Failed to parse YAML from {file_path}: {e}"
            ) from e
        except OSError as e:
            raise FileNotFoundError(
                f"Could not read schema file {file_path}: {e}"
            ) from e

    def parse_language_status(
        self, schema_data: dict[str, Any]
    ) -> list[LanguageImplementation]:
        """Extract language implementation status from parsed schema.

        Args:
            schema_data: Parsed schema dict (from parse_file)

        Returns:
            List of LanguageImplementation TypedDicts

        Raises:
            ValueError: If required fields missing from schema
        """
        if "languages" not in schema_data:
            raise ValueError("Schema missing 'languages' section")

        implementations: list[LanguageImplementation] = []

        for lang_name, lang_data in schema_data["languages"].items():
            if "types" not in lang_data:
                continue  # Skip languages with no type data

            file_format = lang_data.get("file_format", "unknown")

            for type_data in lang_data["types"]:
                impl: LanguageImplementation = {
                    "language": lang_name,
                    "file_format": file_format,
                    "type_name": type_data["name"],
                    "status": type_data.get("status", "unknown"),
                }

                # Extract nested property status if present
                if "properties" in type_data:
                    impl["properties"] = [
                        PropertyStatus(
                            name=prop["name"],
                            status=prop.get("status", "unknown"),
                        )
                        for prop in type_data["properties"]
                    ]

                implementations.append(impl)

        return implementations

    def parse_schema_types(
        self, schema_data: dict[str, Any]
    ) -> list[SchemaType]:
        """Extract type definitions from parsed schema.

        Args:
            schema_data: Parsed schema dict (from parse_file)

        Returns:
            List of SchemaType TypedDicts

        Raises:
            ValueError: If required fields missing
        """
        if "types" not in schema_data:
            raise ValueError("Schema missing 'types' section")

        types: list[SchemaType] = []

        for type_data in schema_data["types"]:
            schema_type: SchemaType = {
                "name": type_data["name"]
            }

            # Optional fields
            if "description" in type_data:
                schema_type["description"] = type_data["description"]

            if "properties" in type_data:
                schema_type["properties"] = type_data["properties"]

            types.append(schema_type)

        return types
