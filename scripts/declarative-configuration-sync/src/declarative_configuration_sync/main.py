"""Main CLI entry point for declarative configuration documentation sync.

This module orchestrates the complete pipeline:
1. GitHub API fetching of schema files
2. Schema discovery via inventory manager
3. YAML parsing
4. Content generation
5. Marker-based injection into target documentation files
6. npm formatting for Prettier compliance
"""

import argparse
import logging
import os
import subprocess
import sys
import tempfile
from collections import defaultdict
from pathlib import Path

import yaml

from declarative_configuration_sync.content_generator import ContentGenerator
from declarative_configuration_sync.github_fetcher import GitHubSchemaFetcher
from declarative_configuration_sync.inventory_manager import InventoryManager
from declarative_configuration_sync.marker_updater import MarkerUpdater
from declarative_configuration_sync.schema_parser import SchemaParser
from declarative_configuration_sync.type_defs import LanguageImplementation

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


def configure_logging() -> None:
    """Configure logging with INFO level and simple format."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )


def main() -> None:
    """Update declarative configuration documentation.

    Accepts --mode argument to specify sync mode:
    - lang-status: Sync language implementation status from main branch
    - types: Sync type documentation from latest release
    """
    configure_logging()

    parser = argparse.ArgumentParser(
        description="Update OpenTelemetry declarative configuration documentation",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--mode",
        choices=["lang-status", "types"],
        required=True,
        help="Sync mode: lang-status (from main branch) or types (from latest release)",
    )
    args = parser.parse_args()

    logger.info("=" * 60)
    logger.info("Declarative Configuration Documentation Sync")
    logger.info("=" * 60)
    logger.info("")

    # Find and change to repository root
    try:
        repo_root = find_repo_root()
        logger.info(f"Repository root: {repo_root}")
        os.chdir(repo_root)
        logger.info(f"Changed working directory to: {Path.cwd()}")
    except RuntimeError as e:
        logger.error(f"❌ {e}")
        sys.exit(1)

    # Initialize GitHub API clients
    logger.info("\nInitializing GitHub API clients...")
    fetcher = GitHubSchemaFetcher()
    inventory_manager = InventoryManager()

    # Determine Git ref based on sync mode
    logger.info("\nDetermining Git ref for sync mode...")
    try:
        if args.mode == "types":
            # For types sync, fetch from latest release
            ref = fetcher.fetch_latest_release()
            logger.info(f"Syncing types documentation from release: {ref}")
        else:
            # For lang-status sync, fetch from main branch
            ref = "main"
            logger.info("Syncing language implementation status from main branch")
    except RuntimeError as e:
        logger.error(f"❌ {e}")
        sys.exit(1)

    # Discover schemas
    logger.info("\nDiscovering schema files via GitHub API...")
    try:
        schema_paths = inventory_manager.discover_schemas()
        logger.info(f"Found {len(schema_paths)} schema files")
    except RuntimeError as e:
        logger.error(f"❌ {e}")
        sys.exit(1)

    # Parse and generate for each schema
    logger.info("\nGenerating documentation...")
    parser_obj = SchemaParser()
    generator = ContentGenerator()
    updater = MarkerUpdater()

    for schema_path in schema_paths:
        schema_name = Path(schema_path).name
        logger.info(f"Processing {schema_name}...")

        try:
            # Fetch schema content from GitHub API
            yaml_content = fetcher.fetch_file_content(schema_path, ref=ref)

            # Write to temporary file for parsing
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".yaml", delete=False
            ) as tmp_file:
                tmp_file.write(yaml_content)
                tmp_path = Path(tmp_file.name)

            try:
                # Parse YAML from temp file
                with open(tmp_path) as f:
                    schema_data = yaml.safe_load(f)

                # Parse schema
                implementations = parser_obj.parse_language_status(schema_data)
                types = parser_obj.parse_schema_types(schema_data)

                # Group implementations by language for accordion generation
                implementations_by_language: dict[
                    str, list[LanguageImplementation]
                ] = defaultdict(list)
                for impl in implementations:
                    implementations_by_language[impl["language"]].append(impl)

                # Generate markdown
                language_content = generator.generate_language_status_accordion(
                    implementations_by_language
                )
                type_content = generator.generate_type_table(types)

                # Update target files
                lang_status_file = (
                    repo_root
                    / "content/en/docs/languages/sdk-configuration"
                    / "language-implementation-status.md"
                )
                types_file = (
                    repo_root
                    / "content/en/docs/languages/sdk-configuration"
                    / "types.md"
                )

                updater.update_file(
                    lang_status_file, "language-implementation-status", language_content
                )
                updater.update_file(types_file, "types", type_content)

                logger.info(f"✓ Updated documentation for {schema_name}")
            finally:
                # Clean up temporary file
                tmp_path.unlink(missing_ok=True)

        except Exception as e:
            logger.error(f"❌ Failed to process {schema_name}: {e}")
            sys.exit(1)

    # Format generated content
    logger.info("\nFormatting generated content...")
    if not run_npm_formatter(repo_root):
        logger.warning("⚠️  Formatting failed but continuing...")

    logger.info("\n✅ Done!")


if __name__ == "__main__":
    main()
