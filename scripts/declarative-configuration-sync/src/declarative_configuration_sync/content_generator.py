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

    def generate_language_status_table(
        self, implementations: list[LanguageImplementation], language: str
    ) -> str:
        """Generate status table for a single language.

        Args:
            implementations: List of implementations for this language
            language: Language name (e.g., "cpp", "java")

        Returns:
            Markdown table section for one language
        """
        if not implementations:
            return ""

        # Extract file format from first implementation (all same language)
        file_format = implementations[0]["file_format"] if implementations else "unknown"

        # Sort by type name for consistent ordering
        sorted_impls = sorted(implementations, key=lambda x: x["type_name"])

        lines = [
            f"### {language} {{#{language}}}",
            "",
            f"Latest supported file format: `{file_format}`",
            "",
            "| Type | Status | Notes | Support Status Details |",
            "|---|---|---|---|",
        ]

        for impl in sorted_impls:
            lines.append(self.generate_table_row(impl))

        return "\n".join(lines)

    def generate_language_status_accordion(
        self, implementations_by_language: dict[str, list[LanguageImplementation]]
    ) -> str:
        """Generate accordion-wrapped tables for all languages.

        Args:
            implementations_by_language: Dict mapping language name to implementations

        Returns:
            Complete accordion section with Hugo shortcode wrapper
        """
        lines = [
            "{{< sdk-lang-status-accordion >}}",
            "",
            '<div class="language-implementation-status-content" style="display: none;">',
            "",
        ]

        # Sort languages alphabetically
        for language in sorted(implementations_by_language.keys()):
            impls = implementations_by_language[language]
            table = self.generate_language_status_table(impls, language)
            if table:
                lines.append(table)
                lines.append("")  # Blank line between languages

        lines.append("</div>")

        return "\n".join(lines)

    def generate_type_table(self, types: list[SchemaType]) -> str:
        """Generate type documentation table.

        Args:
            types: List of schema type definitions

        Returns:
            Markdown table with type descriptions and properties
        """
        if not types:
            return ""

        lines = ["| Type | Description | Properties |", "|---|---|---|"]

        # Sort by type name for consistent ordering
        sorted_types = sorted(types, key=lambda x: x["name"])

        for schema_type in sorted_types:
            name = schema_type["name"]
            # Type name with anchor link
            type_link = f"[`{name}`](#{name.lower()})"

            # Description (optional, escaped)
            description = self.escape_markdown_table_content(schema_type.get("description", ""))

            # Properties list (optional)
            properties = schema_type.get("properties", [])
            props_str = ", ".join(f"`{p}`" for p in properties) if properties else ""

            lines.append(f"| {type_link} | {description} | {props_str} |")

        return "\n".join(lines)
