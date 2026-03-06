"""GitHub API integration for fetching schema files.

Fetches YAML schema files from opentelemetry-configuration repository
via GitHub API without requiring local git clone.
"""

import logging
from typing import Final

import requests
from requests.exceptions import ConnectionError, RequestException, Timeout

logger = logging.getLogger(__name__)


class GitHubSchemaFetcher:
    """Fetches schema files from GitHub API.

    Uses GitHub contents API to fetch raw YAML schema files from
    opentelemetry-configuration repository.

    Attributes:
        REPO_OWNER: GitHub organization name
        REPO_NAME: Repository name
        SCHEMA_PATH: Path to schema directory in repo
        API_BASE: GitHub API base URL
    """

    REPO_OWNER: Final[str] = "open-telemetry"
    REPO_NAME: Final[str] = "opentelemetry-configuration"
    SCHEMA_PATH: Final[str] = "schema"
    API_BASE: Final[str] = "https://api.github.com"

    def __init__(self, timeout: int = 30) -> None:
        """Initialize GitHub fetcher.

        Args:
            timeout: Request timeout in seconds (default: 30)
        """
        self.timeout = timeout

    def fetch_latest_release(self) -> str:
        """Fetch latest release tag from opentelemetry-configuration repository.

        Returns:
            Release tag name (e.g., "v0.1.0")

        Raises:
            RuntimeError: If GitHub API request fails or no releases found
        """
        url = f"{self.API_BASE}/repos/{self.REPO_OWNER}/{self.REPO_NAME}/releases/latest"
        headers = {
            "Accept": "application/vnd.github+json",
        }

        logger.info("Fetching latest release from GitHub API")

        try:
            response = requests.get(
                url,
                headers=headers,
                timeout=self.timeout,
            )
            response.raise_for_status()

            data = response.json()
            tag_name = data.get("tag_name")

            if not tag_name:
                error_msg = "GitHub API response missing 'tag_name' field"
                logger.error(error_msg)
                raise RuntimeError(error_msg)

            logger.info(f"Latest release: {tag_name}")
            return tag_name

        except Timeout as e:
            error_msg = f"Request timeout after {self.timeout}s while fetching latest release"
            logger.error(error_msg)
            raise RuntimeError(error_msg) from e

        except ConnectionError as e:
            error_msg = f"Network error while fetching latest release: {e}"
            logger.error(error_msg)
            raise RuntimeError(error_msg) from e

        except requests.exceptions.HTTPError as e:
            if e.response is not None:
                status_code = e.response.status_code
                if status_code == 404:
                    error_msg = "No releases found for opentelemetry-configuration repository"
                elif status_code == 403:
                    error_msg = "GitHub API rate limit exceeded or authentication required"
                else:
                    error_msg = f"HTTP {status_code} error while fetching latest release"
            else:
                error_msg = f"HTTP error while fetching latest release: {e}"

            logger.error(error_msg)
            raise RuntimeError(error_msg) from e

        except RequestException as e:
            error_msg = f"Request error while fetching latest release: {e}"
            logger.error(error_msg)
            raise RuntimeError(error_msg) from e

    def fetch_file_content(self, file_path: str, ref: str = "main") -> str:
        """Fetch raw file content from GitHub API.

        Args:
            file_path: Path to file in repository (e.g., "schema/tracer.yaml")
            ref: Git reference (branch, tag, or commit) to fetch from (default: "main")

        Returns:
            Raw file content as string

        Raises:
            RuntimeError: On HTTP errors, timeouts, or network failures

        Example:
            >>> fetcher = GitHubSchemaFetcher()
            >>> content = fetcher.fetch_file_content("schema/tracer.yaml")
            >>> print(content)
            types:
              - name: TracerProvider
                description: Configuration for TracerProvider
        """
        url = f"{self.API_BASE}/repos/{self.REPO_OWNER}/{self.REPO_NAME}/contents/{file_path}"
        params = {"ref": ref}
        headers = {
            "Accept": "application/vnd.github.raw+json",  # Request raw content directly
        }

        logger.info(f"Fetching {file_path} (ref: {ref}) from GitHub API")

        try:
            response = requests.get(
                url,
                params=params,
                headers=headers,
                timeout=self.timeout,
            )
            response.raise_for_status()

            logger.info(f"Successfully fetched {file_path} ({len(response.text)} bytes)")
            return response.text

        except Timeout as e:
            error_msg = f"Request timeout after {self.timeout}s while fetching {file_path}"
            logger.error(error_msg)
            raise RuntimeError(error_msg) from e

        except ConnectionError as e:
            error_msg = f"Network error while fetching {file_path}: {e}"
            logger.error(error_msg)
            raise RuntimeError(error_msg) from e

        except requests.exceptions.HTTPError as e:
            if e.response is not None:
                status_code = e.response.status_code
                if status_code == 404:
                    error_msg = f"File not found: {file_path} (ref: {ref})"
                elif status_code == 403:
                    error_msg = "GitHub API rate limit exceeded or authentication required"
                else:
                    error_msg = f"HTTP {status_code} error while fetching {file_path}"
            else:
                error_msg = f"HTTP error while fetching {file_path}: {e}"

            logger.error(error_msg)
            raise RuntimeError(error_msg) from e

        except RequestException as e:
            error_msg = f"Request error while fetching {file_path}: {e}"
            logger.error(error_msg)
            raise RuntimeError(error_msg) from e
