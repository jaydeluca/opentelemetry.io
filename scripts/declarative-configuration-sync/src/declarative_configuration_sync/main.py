"""Main CLI entry point for declarative configuration documentation sync.

This module orchestrates the complete pipeline:
1. GitHub API fetching of schema files
2. Schema discovery via inventory manager
3. YAML parsing
4. Content generation
5. Marker-based injection into target documentation files
6. npm formatting for Prettier compliance
"""

import logging
import os
import subprocess
import sys
from pathlib import Path

logger = logging.getLogger(__name__)


def find_repo_root() -> Path:
    """Find the opentelemetry.io repository root.

    Searches upward from current directory for Hugo indicators.

    Returns:
        Path to repository root

    Raises:
        RuntimeError: If repository root cannot be found
    """
    current = Path.cwd()

    # Search upward for repo root indicators
    for path in [current, *current.parents]:
        # Hugo config is in config/_default/ and content is in content/en/
        has_hugo_config = (path / "config" / "_default").exists()
        has_content = (path / "content" / "en").exists()

        if has_hugo_config and has_content:
            return path

    raise RuntimeError(
        "Could not find opentelemetry.io repository root. "
        "Please run from within the repository "
        "(looking for config/_default/ and content/en/)."
    )


def run_npm_formatter(repo_root: Path) -> bool:
    """Run npm fix:format to format generated content.

    Args:
        repo_root: Path to repository root

    Returns:
        True if formatting succeeded, False otherwise
    """
    logger.info("Running npm fix:format...")

    try:
        result = subprocess.run(
            ["npm", "run", "fix:format"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            timeout=300,  # 5 minute timeout
            check=False,  # Don't raise on non-zero exit
        )

        if result.returncode == 0:
            logger.info("✓ Formatting complete")
            return True
        else:
            logger.error(f"Formatting failed: {result.stderr}")
            return False

    except subprocess.TimeoutExpired:
        logger.error("Formatting timeout after 5 minutes")
        return False
    except FileNotFoundError:
        logger.error("npm command not found - is Node.js installed?")
        return False
    except Exception as e:
        logger.error(f"Unexpected error running formatter: {e}")
        return False
