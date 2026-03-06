"""InventoryManager for discovering schema files via GitHub API.

This module provides functionality to discover YAML schema files from the
opentelemetry-configuration repository using the GitHub API tree endpoint,
filtering out meta-schema tracking files.
"""

import logging

import requests
from requests.exceptions import RequestException

logger = logging.getLogger(__name__)


class InventoryManager:
    """Manages discovery of schema files from GitHub repository.

    Uses GitHub API /contents endpoint to list files in the schema directory,
    filtering to include only YAML schema files while excluding meta-schema
    tracking files (files starting with "meta_schema_").

    Attributes:
        REPO_OWNER: GitHub repository owner (open-telemetry)
        REPO_NAME: GitHub repository name (opentelemetry-configuration)
        SCHEMA_PATH: Path to schema directory in repository
        API_BASE: Base URL for GitHub API
    """

    REPO_OWNER = "open-telemetry"
    REPO_NAME = "opentelemetry-configuration"
    SCHEMA_PATH = "schema"
    API_BASE = "https://api.github.com"

    def __init__(self, ref: str = "main", timeout: int = 30) -> None:
        """Initialize InventoryManager.

        Args:
            ref: Git reference (branch, tag, or commit SHA) to fetch from
            timeout: Request timeout in seconds
        """
        self.ref = ref
        self.timeout = timeout

    def discover_schemas(self) -> list[str]:
        """Discover schema files from GitHub repository.

        Fetches file listing from GitHub API, filters to include only .yaml files
        in the schema directory while excluding meta-schema files (files starting
        with "meta_schema_"). Returns sorted list of file paths.

        Returns:
            Sorted list of schema file paths (e.g., ["schema/logger.yaml", ...])

        Raises:
            RuntimeError: If GitHub API request fails or returns error status
        """
        url = (
            f"{self.API_BASE}/repos/{self.REPO_OWNER}/{self.REPO_NAME}"
            f"/contents/{self.SCHEMA_PATH}"
        )
        params = {"ref": self.ref}

        try:
            response = requests.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
        except RequestException as e:
            raise RuntimeError(
                f"Failed to fetch schema list from GitHub API: {e}"
            ) from e

        # Parse response - GitHub /contents endpoint returns list of file/dir objects
        files = response.json()

        # Filter to include only .yaml schema files, excluding meta-schema files
        schema_paths = [
            file_obj["path"]
            for file_obj in files
            if file_obj["type"] == "file"
            and file_obj["name"].endswith(".yaml")
            and not file_obj["name"].startswith("meta_schema_")
        ]

        # Sort for consistent output
        schema_paths.sort()

        logger.info("Discovered %d schema files from %s", len(schema_paths), url)

        return schema_paths
