"""
FormFiller - Fill PDF forms with data from CSV files.

Refactored main module using modular architecture with proper separation of concerns.
"""

import logging
import sys
from pathlib import Path

from cli import CLI
from config import FormFillerConfig
from exceptions import FormFillerError
from form_filler import FormFiller


def setup_logging(verbose: bool = False) -> None:
    """
    Set up logging configuration.

    Args:
        verbose: Whether to enable verbose logging
    """
    level = logging.DEBUG if verbose else logging.INFO
    format_str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    logging.basicConfig(
        level=level,
        format=format_str,
        handlers=[
            logging.StreamHandler(sys.stdout),
        ],
    )


def main() -> int:
    """
    Main entry point for the FormFiller application.

    Returns:
        Exit code (0 for success, non-zero for failure)
    """
    cli = CLI()

    try:
        # Parse and validate command-line arguments
        args = cli.parse_args()

        # Setup logging
        setup_logging(verbose=args.verbose)
        logger = logging.getLogger(__name__)

        logger.info("FormFiller application started")

        # Validate arguments
        cli.validate_args(args)

        # Initialize FormFiller with configuration
        config = FormFillerConfig(base_path=str(Path.cwd()))
        form_filler = FormFiller(config=config)

        # Validate template before processing
        logger.info(f"Validating template: {args.template_config.name}")
        validation_results = form_filler.validate_template(args.template_config)
        logger.debug(f"Template validation results: {validation_results}")

        # Process forms
        logger.info(f"Processing forms from {args.input_file}")
        results = form_filler.process_forms(
            input_csv_path=args.input_file_path,
            template_config=args.template_config,
            skip_header=args.skip_header,
            dry_run=args.dry_run,
            generate_combined_pdf=True,
        )

        # Print results
        print("\\nFormFiller completed successfully!")
        print(f"Template used: {results['template_used']}")
        print(f"Total rows processed: {results['total_rows']}")
        print(f"Successful fills: {results['successful_fills']}")

        if results["failed_fills"] > 0:
            print(f"Failed fills: {results['failed_fills']}")

        if "combined_pdf_path" in results:
            print(f"Combined PDF saved to: {results['combined_pdf_path']}")

        # Print mapping statistics
        mapping_stats = results["mapping_summary"]
        print("\\nMapping statistics:")
        print(f"  Active fields: {mapping_stats['active_fields']}")
        print(f"  Total fields: {mapping_stats['total_fields']}")
        print(f"  Multi-column fields: {mapping_stats['multi_column_fields']}")

        if args.dry_run:
            print("\\n[DRY RUN] No actual PDF files were generated.")

        logger.info("FormFiller application completed successfully")
        return 0

    except KeyboardInterrupt:
        print("\\nOperation cancelled by user.")
        return 130
    except FormFillerError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        logging.getLogger(__name__).exception("Unexpected error occurred")
        return 2


if __name__ == "__main__":
    sys.exit(main())
