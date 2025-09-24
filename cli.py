"""Command-line interface for FormFiller application."""

import argparse
import sys
from pathlib import Path
from typing import List, Optional

from config import FormFillerConfig
from exceptions import FormFillerError


class CLI:
    """Command-line interface handler for FormFiller."""

    def __init__(self):
        """Initialize CLI handler."""
        self.config = FormFillerConfig()
        self.parser = self._create_parser()

    def _create_parser(self) -> argparse.ArgumentParser:
        """Create and configure argument parser."""
        parser = argparse.ArgumentParser(
            description="FormFiller - Fill PDF forms with data from CSV files. "
            "Supports 1099-MISC and 1099-NEC forms at enterprise scale.",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=self._get_usage_examples(),
        )

        parser.add_argument(
            "input_file",
            type=str,
            help="Name of the CSV input file located in the 'inputs' folder. "
            "Examples: misc_example_input.csv, nec_example_input.csv",
        )

        parser.add_argument(
            "--template",
            "-t",
            type=str,
            default="misc",
            help="Template type to use for form filling. "
            f"Built-in options: {', '.join(self.config.list_available_templates().keys())}. "
            "You can also provide a custom template by specifying the full file path. "
            "(default: %(default)s)",
        )

        parser.add_argument(
            "--skip-header",
            "-s",
            action="store_true",
            help="Skip the first row of the CSV file (useful when CSV has column headers). "
            "(default: %(default)s)",
        )

        parser.add_argument(
            "--output-dir",
            "-o",
            type=str,
            help="Output directory for generated PDF files. (default: outputs/)",
        )

        parser.add_argument(
            "--verbose",
            "-v",
            action="store_true",
            help="Enable verbose logging output.",
        )

        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Perform a dry run without generating actual PDF files.",
        )

        return parser

    def _get_usage_examples(self) -> str:
        """Get formatted usage examples."""
        return """
Examples:
  python main.py misc_example_input.csv
  python main.py nec_example_input.csv --template nec
  python main.py mydata.csv --template /path/to/custom_template.pdf --skip-header
  python main.py data.csv --output-dir /custom/output --verbose
        """

    def parse_args(self, args: Optional[List[str]] = None) -> argparse.Namespace:
        """
        Parse command-line arguments.

        Args:
            args: Optional list of arguments to parse (for testing)

        Returns:
            Parsed arguments namespace
        """
        return self.parser.parse_args(args)

    def validate_args(self, args: argparse.Namespace) -> None:
        """
        Validate parsed arguments.

        Args:
            args: Parsed arguments to validate

        Raises:
            FormFillerError: If arguments are invalid
        """
        try:
            # Validate input file exists
            args.input_file_path = self.config.validate_input_file(args.input_file)

            # Validate and get template configuration
            template_config = self.config.get_template_config(args.template)
            args.template_config = template_config

            # Validate template configuration
            if not template_config.validate():
                missing_files = []
                if not Path(template_config.template_path).exists():
                    missing_files.append(f"template: {template_config.template_path}")
                if not Path(template_config.mapping_path).exists():
                    missing_files.append(f"mapping: {template_config.mapping_path}")

                raise FormFillerError(
                    f"Missing required files: {', '.join(missing_files)}"
                )

            # Set output directory if provided
            if args.output_dir:
                self.config.outputs_folder = Path(args.output_dir)

        except Exception as e:
            if isinstance(e, FormFillerError):
                raise
            raise FormFillerError(f"Argument validation failed: {e}")

    def print_help(self) -> None:
        """Print help message."""
        self.parser.print_help()

    def print_available_templates(self) -> None:
        """Print available built-in templates."""
        templates = self.config.list_available_templates()
        print("Available built-in templates:")
        for key, name in templates.items():
            print(f"  {key}: {name}")

    def handle_error(self, error: Exception) -> int:
        """
        Handle and display errors appropriately.

        Args:
            error: Exception that occurred

        Returns:
            Exit code for the application
        """
        if isinstance(error, FormFillerError):
            print(f"Error: {error}", file=sys.stderr)
            return 1
        elif isinstance(error, FileNotFoundError):
            print(f"File not found: {error}", file=sys.stderr)
            return 1
        elif isinstance(error, KeyboardInterrupt):
            print("\\nOperation cancelled by user.", file=sys.stderr)
            return 130
        else:
            print(f"Unexpected error: {error}", file=sys.stderr)
            return 2
