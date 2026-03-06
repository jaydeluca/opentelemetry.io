"""Update existing documentation files with generated content using markers."""

import re
from pathlib import Path


class MarkerUpdater:
    """Updates markdown files by replacing content between HTML comment markers."""

    def __init__(
        self,
        marker_prefix: str = "GENERATED",
        source: str = "declarative-configuration-sync"
    ):
        """Initialize marker updater.

        Args:
            marker_prefix: Prefix for marker comments (default: "GENERATED")
            source: Source identifier for the markers
        """
        self.marker_prefix = marker_prefix
        self.source = source

    def get_marker_pattern(self, marker_id: str) -> tuple[str, str]:
        """Get the begin and end marker strings for a given marker ID.

        Args:
            marker_id: Unique identifier for the marker

        Returns:
            Tuple of (begin_marker, end_marker)
        """
        begin = f"<!-- BEGIN {self.marker_prefix}: {marker_id} SOURCE: {self.source} -->"
        end = f"<!-- END {self.marker_prefix}: {marker_id} SOURCE: {self.source} -->"
        return begin, end

    def _build_marker_regex(self, marker_id: str) -> re.Pattern:
        """Build regex pattern to match marker section.

        Matches patterns like:
            <!-- BEGIN GENERATED: marker-id -->
            <!-- BEGIN GENERATED: marker-id SOURCE: declarative-configuration-sync -->

        Args:
            marker_id: Marker identifier

        Returns:
            Compiled regex pattern
        """
        # Escape special regex characters in prefix and marker_id
        begin_pattern = (
            re.escape(f"<!-- BEGIN {self.marker_prefix}: {marker_id}")
            + r"(?:\s+SOURCE:\s+[\w\-/.]+)?"  # Optional SOURCE attribute
            + re.escape(" -->")
        )
        end_pattern = (
            re.escape(f"<!-- END {self.marker_prefix}: {marker_id}")
            + r"(?:\s+SOURCE:\s+[\w\-/.]+)?"  # Optional SOURCE attribute
            + re.escape(" -->")
        )

        # DOTALL flag makes . match newlines
        pattern = begin_pattern + r".*?" + end_pattern
        return re.compile(pattern, re.DOTALL)

    def update_section(
        self,
        content: str,
        marker_id: str,
        new_content: str
    ) -> tuple[str, bool]:
        """Update a section of content between markers.

        Args:
            content: Original markdown content
            marker_id: Marker identifier
            new_content: New content to insert between markers

        Returns:
            Tuple of (updated_content, was_updated)
            was_updated is False if markers weren't found
        """
        begin_marker, end_marker = self.get_marker_pattern(marker_id)
        regex = self._build_marker_regex(marker_id)

        if not regex.search(content):
            return content, False

        replacement = f"{begin_marker}\n{new_content}\n{end_marker}"
        updated_content = regex.sub(replacement, content)

        return updated_content, True
