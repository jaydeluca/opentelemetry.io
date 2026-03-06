"""Markdown content generator for configuration schema documentation."""

from declarative_configuration_sync.type_defs import (
    LanguageImplementation,
    PropertyStatus,
    SchemaType,
)


class ContentGenerator:
    """Generates markdown tables from parsed schema data."""

    @staticmethod
    def escape_markdown_table_content(text: str) -> str:
        """Escape special characters for markdown table cells.

        Args:
            text: Raw text to escape

        Returns:
            Escaped text safe for table cells
        """
        # Pipe characters break table formatting
        return text.replace("|", "\\|")

    @staticmethod
    def generate_property_status_cell(properties: list[PropertyStatus]) -> str:
        """Generate nested property list for table cell.

        Args:
            properties: List of property status dicts

        Returns:
            HTML-formatted bullet list with line breaks
        """
        if not properties:
            return ""

        # Use HTML entities and <br> tags as seen in target page
        escaped_props = [
            f"• `{ContentGenerator.escape_markdown_table_content(p['name'])}`: {p['status']}"
            for p in properties
        ]
        return "<br>".join(escaped_props)

    @staticmethod
    def generate_table_row(impl: LanguageImplementation) -> str:
        """Generate single table row for language implementation.

        Args:
            impl: Language implementation data

        Returns:
            Markdown table row
        """
        # Type name with link to types page (anchor is lowercase)
        type_link = f"[`{impl['type_name']}`](../types#{impl['type_name'].lower()})"

        # Status column
        status = impl["status"]

        # Notes column (empty for now, reserved for future use)
        notes = ""

        # Support status details with nested properties
        props = ContentGenerator.generate_property_status_cell(impl.get("properties", []))
        # Add leading space for empty properties to maintain table alignment
        details = f" {props} " if props else "  "

        return f"| {type_link} | {status} | {notes} | {details}|"
