"""Pytest configuration to ensure proper module imports."""

import sys
from pathlib import Path

# Add src directory to Python path so tests can import documentation_sync
src_dir = Path(__file__).parent / "src"
sys.path.insert(0, str(src_dir))
