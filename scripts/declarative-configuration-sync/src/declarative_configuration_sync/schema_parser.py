"""YAML schema parser for OpenTelemetry configuration schemas."""

import yaml
from pathlib import Path
from typing import Any


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
