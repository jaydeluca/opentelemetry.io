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


class TestFileUpdateOperations:
    """Test file I/O operations."""

    def test_update_file_successfully_updates_and_returns_true(self, tmp_path, sample_content):
        """Test that update_file successfully updates file and returns True."""
        test_file = tmp_path / "test.md"
        test_file.write_text(sample_content, encoding="utf-8")

        updater = MarkerUpdater()
        result = updater.update_file(test_file, "test-section", "NEW FILE CONTENT")

        assert result is True
        updated_content = test_file.read_text(encoding="utf-8")
        assert "NEW FILE CONTENT" in updated_content
        assert "Old generated content" not in updated_content

    def test_update_file_returns_false_when_markers_not_found(self, tmp_path, sample_content):
        """Test that update_file returns False when markers not found."""
        test_file = tmp_path / "test.md"
        original_content = sample_content
        test_file.write_text(original_content, encoding="utf-8")

        updater = MarkerUpdater()
        result = updater.update_file(test_file, "nonexistent-marker", "NEW CONTENT")

        assert result is False
        # File should be unchanged
        assert test_file.read_text(encoding="utf-8") == original_content

    def test_update_file_raises_filenotfound_for_missing_files(self, tmp_path):
        """Test that update_file raises FileNotFoundError for missing files."""
        missing_file = tmp_path / "missing.md"

        updater = MarkerUpdater()
        with pytest.raises(FileNotFoundError, match="File not found"):
            updater.update_file(missing_file, "test-section", "NEW CONTENT")

    def test_update_file_preserves_utf8_encoding(self, tmp_path):
        """Test that update_file preserves UTF-8 encoding."""
        content = """
<!-- BEGIN GENERATED: test -->
old content
<!-- END GENERATED: test -->

Unicode content: 日本語 español français
"""
        test_file = tmp_path / "test.md"
        test_file.write_text(content, encoding="utf-8")

        updater = MarkerUpdater()
        result = updater.update_file(test_file, "test", "新しい内容")

        assert result is True
        updated_content = test_file.read_text(encoding="utf-8")
        assert "新しい内容" in updated_content
        assert "日本語 español français" in updated_content

    def test_update_multiple_sections_updates_all_markers(self):
        """Test that update_multiple_sections updates all markers in dict."""
        content = """
<!-- BEGIN GENERATED: section-one -->
content one
<!-- END GENERATED: section-one -->

Some text in between.

<!-- BEGIN GENERATED: section-two -->
content two
<!-- END GENERATED: section-two -->

<!-- BEGIN GENERATED: section-three -->
content three
<!-- END GENERATED: section-three -->
"""
        updater = MarkerUpdater()
        updates = {
            "section-one": "UPDATED ONE",
            "section-two": "UPDATED TWO",
            "section-three": "UPDATED THREE",
        }

        updated, results = updater.update_multiple_sections(content, updates)

        assert results["section-one"] is True
        assert results["section-two"] is True
        assert results["section-three"] is True
        assert "UPDATED ONE" in updated
        assert "UPDATED TWO" in updated
        assert "UPDATED THREE" in updated
        assert "content one" not in updated
        assert "content two" not in updated
        assert "content three" not in updated
        assert "Some text in between." in updated  # Preserved

    def test_update_multiple_sections_reports_per_marker_success(self):
        """Test that update_multiple_sections reports per-marker success/failure."""
        content = """
<!-- BEGIN GENERATED: exists -->
old content
<!-- END GENERATED: exists -->
"""
        updater = MarkerUpdater()
        updates = {
            "exists": "NEW CONTENT",
            "missing": "OTHER CONTENT",
        }

        updated, results = updater.update_multiple_sections(content, updates)

        assert results["exists"] is True
        assert results["missing"] is False
        assert "NEW CONTENT" in updated
        assert "OTHER CONTENT" not in updated
