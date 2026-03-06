"""Tests for MarkerUpdater class."""

from pathlib import Path

import pytest

from declarative_configuration_sync.marker_updater import MarkerUpdater


@pytest.fixture
def sample_content():
    """Load sample markdown content."""
    fixture_path = Path(__file__).parent / "fixtures" / "sample_markdown.md"
    return fixture_path.read_text()


class TestMarkerPatternMatching:
    """Test marker pattern matching functionality."""

    def test_update_section_with_source_attribute(self, sample_content):
        """Test that update_section finds and replaces content with SOURCE attribute."""
        updater = MarkerUpdater()
        new_content = "NEW GENERATED CONTENT"

        updated, was_updated = updater.update_section(
            sample_content,
            "test-section",
            new_content
        )

        assert was_updated is True
        assert new_content in updated
        assert "Old generated content" not in updated

    def test_update_section_legacy_format_without_source(self, sample_content):
        """Test that pattern matches legacy format without SOURCE attribute."""
        updater = MarkerUpdater()
        new_content = "UPDATED LEGACY CONTENT"

        updated, was_updated = updater.update_section(
            sample_content,
            "legacy-section",
            new_content
        )

        assert was_updated is True
        assert new_content in updated
        assert "Legacy format without SOURCE" not in updated

    def test_update_section_preserves_content_outside_markers(self, sample_content):
        """Test that all content outside markers is preserved."""
        updater = MarkerUpdater()

        updated, was_updated = updater.update_section(
            sample_content,
            "test-section",
            "NEW CONTENT"
        )

        assert was_updated is True
        # Check all manual content is preserved
        assert "## Manual Content" in updated
        assert "This content should be preserved." in updated
        assert "More manual content here." in updated
        assert "Final manual content." in updated
        # Check frontmatter preserved
        assert "title: Test Page" in updated

    def test_update_section_returns_false_when_markers_not_found(self, sample_content):
        """Test that update_section returns (content, False) when markers not found."""
        updater = MarkerUpdater()

        updated, was_updated = updater.update_section(
            sample_content,
            "nonexistent-marker",
            "NEW CONTENT"
        )

        assert was_updated is False
        assert updated == sample_content  # Content unchanged

    def test_marker_id_matching_is_case_sensitive(self):
        """Test that marker_id matching is case-sensitive."""
        content = """
<!-- BEGIN GENERATED: MySection -->
old content
<!-- END GENERATED: MySection -->
"""
        updater = MarkerUpdater()

        # Try to update with different case
        updated, was_updated = updater.update_section(
            content,
            "mysection",  # lowercase
            "new content"
        )

        assert was_updated is False
        assert "old content" in updated

    def test_multiple_markers_update_independently(self):
        """Test that multiple markers in same content can be updated independently."""
        content = """
<!-- BEGIN GENERATED: section-one -->
content one
<!-- END GENERATED: section-one -->

<!-- BEGIN GENERATED: section-two -->
content two
<!-- END GENERATED: section-two -->
"""
        updater = MarkerUpdater()

        # Update only section-one
        updated, was_updated = updater.update_section(
            content,
            "section-one",
            "UPDATED ONE"
        )

        assert was_updated is True
        assert "UPDATED ONE" in updated
        assert "content two" in updated  # section-two unchanged
        assert "content one" not in updated
