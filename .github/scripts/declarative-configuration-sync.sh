#!/bin/bash
set -e
set -o pipefail

# This script synchronizes OpenTelemetry SDK configuration documentation
# from the opentelemetry-configuration repository.

# Validate required environment variables
if [ -z "$GH_TOKEN" ]; then
  echo "Error: GH_TOKEN environment variable is required" >&2
  exit 1
fi

# Check gh CLI authentication
gh auth status >/dev/null 2>&1 || {
  echo "Error: gh CLI authentication failed" >&2
  exit 1
}

if [ -z "$GITHUB_REPOSITORY" ]; then
  echo "Error: GITHUB_REPOSITORY environment variable is required" >&2
  exit 1
fi

# Parse --mode argument
MODE="lang-status"  # Default mode
if [ -n "$1" ]; then
  MODE="${1#--mode=}"
fi

# Validate mode
if [[ "$MODE" != "lang-status" && "$MODE" != "types" ]]; then
  echo "Error: Invalid mode '$MODE'. Must be 'lang-status' or 'types'" >&2
  exit 1
fi

echo "Starting declarative configuration documentation sync (mode: ${MODE})"

# Install Node.js dependencies
echo "Installing Node.js dependencies..."
npm install --omit=optional

# Install Python dependencies
echo "Installing Python dependencies..."
cd scripts/declarative-configuration-sync || {
  echo "Error: Failed to change to scripts/declarative-configuration-sync directory" >&2
  exit 1
}
uv sync

# Generate documentation
echo "Generating documentation (mode: ${MODE})..."
uv run python -m declarative_configuration_sync --mode="${MODE}" || {
  echo "Error: Documentation generation failed with mode '${MODE}'" >&2
  exit 1
}

# Return to repo root
cd ../.. || {
  echo "Error: Failed to return to repo root" >&2
  exit 1
}

# Format generated documentation
echo "Formatting documentation..."
npm run fix:format

# Skip link checking - configuration sync doesn't modify external links
# This differs from collector-sync which clones external repos that may contain broken links

echo "Declarative configuration documentation sync complete (mode: ${MODE})"
