"""Configuration management for FormFiller application."""

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional


@dataclass
class TemplateConfig:
    """Configuration for PDF template and field mapping."""

    name: str
    template_path: str
    mapping_path: str
    output_prefix: str

    def validate(self) -> bool:
        """Validate that all required files exist."""
        return os.path.exists(self.template_path) and os.path.exists(self.mapping_path)


class FormFillerConfig:
    """Main configuration class for FormFiller application."""

    # Built-in template configurations
    BUILT_IN_TEMPLATES = {
        "misc": TemplateConfig(
            name="1099-MISC",
            template_path="templates/1099_page_3.pdf",
            mapping_path="misc_field_number_mapping.yml",
            output_prefix="misc_big",
        ),
        "nec": TemplateConfig(
            name="1099-NEC",
            template_path="templates/nec_template.pdf",
            mapping_path="nec_fnm.yml",
            output_prefix="nec_big",
        ),
    }

    def __init__(self, base_path: Optional[str] = None):
        """Initialize configuration with optional base path."""
        self.base_path = Path(base_path) if base_path else Path.cwd()
        self.inputs_folder = self.base_path / "inputs"
        self.outputs_folder = self.base_path / "outputs"
        self.templates_folder = self.base_path / "templates"

    def get_template_config(self, template_name: str) -> TemplateConfig:
        """Get template configuration by name or path."""
        if template_name in self.BUILT_IN_TEMPLATES:
            config = self.BUILT_IN_TEMPLATES[template_name]
            # Make paths absolute based on base_path
            config.template_path = str(self.base_path / config.template_path)
            config.mapping_path = str(self.base_path / config.mapping_path)
            return config
        else:
            # Treat as custom template path
            return TemplateConfig(
                name="custom",
                template_path=template_name,
                mapping_path=str(self.base_path / "field_number_mapping_custom.yml"),
                output_prefix="custom_big",
            )

    def validate_input_file(self, filename: str) -> str:
        """Validate and return full path to input CSV file."""
        input_path = self.inputs_folder / filename
        if not input_path.exists():
            available_files = [
                f.name for f in self.inputs_folder.glob("*.csv") if f.is_file()
            ]
            raise FileNotFoundError(
                f"Input file '{input_path}' does not exist.\n"
                f"Available files: {', '.join(available_files)}"
            )
        return str(input_path)

    def get_output_path(self, filename: str) -> str:
        """Get full output path, creating directory if needed."""
        output_path = self.outputs_folder / filename
        output_path.parent.mkdir(parents=True, exist_ok=True)
        return str(output_path)

    def get_big_output_path(self, output_prefix: str) -> str:
        """Get path for combined output file."""
        big_output_path = self.outputs_folder / "big" / f"{output_prefix}.pdf"
        big_output_path.parent.mkdir(parents=True, exist_ok=True)
        return str(big_output_path)

    @classmethod
    def list_available_templates(cls) -> Dict[str, str]:
        """List all available built-in templates."""
        return {name: config.name for name, config in cls.BUILT_IN_TEMPLATES.items()}
