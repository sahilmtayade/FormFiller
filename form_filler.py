"""Core FormFiller application class."""

import logging
import os
from typing import Optional

import fitz

from config import FormFillerConfig, TemplateConfig
from data_processor import DataProcessor
from exceptions import DataProcessingError, FormFillerError, TemplateError
from utils.fill_form import fill_form

logger = logging.getLogger(__name__)


class FormFiller:
    """
    Main FormFiller application class.

    Handles the core functionality of filling PDF forms with CSV data.
    """

    def __init__(self, config: Optional[FormFillerConfig] = None):
        """
        Initialize FormFiller application.

        Args:
            config: Optional configuration object. If None, creates default config.
        """
        self.config = config or FormFillerConfig()
        self.data_processor = DataProcessor()
        self._filled_count = 0

    def process_forms(
        self,
        input_csv_path: str,
        template_config: TemplateConfig,
        skip_header: bool = False,
        dry_run: bool = False,
        generate_combined_pdf: bool = True,
    ) -> dict:
        """
        Process CSV data and fill PDF forms.

        Args:
            input_csv_path: Path to input CSV file
            template_config: Template configuration
            skip_header: Whether to skip the first row of CSV
            dry_run: If True, don't actually create PDF files
            generate_combined_pdf: If True, create a combined PDF with all forms

        Returns:
            Dictionary with processing results and statistics

        Raises:
            FormFillerError: If processing fails
        """
        try:
            # Load data and mappings
            logger.info(f"Loading CSV data from {input_csv_path}")
            self.data_processor.load_csv_data(input_csv_path)

            logger.info(f"Loading field mappings from {template_config.mapping_path}")
            self.data_processor.load_field_mappings(template_config.mapping_path)

            # Process all data
            logger.info("Processing CSV data with field mappings")
            processed_data = self.data_processor.process_all_data(
                skip_header=skip_header
            )

            if not processed_data:
                raise DataProcessingError("No valid data rows found to process")

            # Initialize combined PDF document if requested
            combined_doc = None
            if generate_combined_pdf and not dry_run:
                combined_doc = fitz.open()

            # Process each row and generate PDFs
            self._filled_count = 0
            failed_count = 0

            for i, field_data in enumerate(processed_data):
                try:
                    if dry_run:
                        logger.info(
                            f"[DRY RUN] Would process row {i + 1} with {len(field_data)} fields"
                        )
                        self._filled_count += 1
                        continue

                    # Generate individual PDF
                    output_path = self.config.get_output_path(f"{i}.pdf")

                    logger.debug(f"Filling form for row {i + 1}, output: {output_path}")
                    fill_form(
                        pdf_path=template_config.template_path,
                        field_data=field_data,
                        output_pdf_path=output_path,
                        new_doc=combined_doc,
                    )
                    self._filled_count += 1

                except Exception as e:
                    logger.error(f"Failed to process row {i + 1}: {e}")
                    failed_count += 1
                    continue

            # Save combined PDF if created
            if combined_doc and not dry_run:
                combined_output_path = self.config.get_big_output_path(
                    template_config.output_prefix
                )
                logger.info(f"Saving combined PDF to {combined_output_path}")
                combined_doc.save(combined_output_path)
                combined_doc.close()

            # Return processing results
            results = {
                "total_rows": len(processed_data),
                "successful_fills": self._filled_count,
                "failed_fills": failed_count,
                "template_used": template_config.name,
                "dry_run": dry_run,
                "mapping_summary": self.data_processor.get_mapping_summary(),
            }

            if generate_combined_pdf and not dry_run:
                results["combined_pdf_path"] = combined_output_path

            logger.info(
                f"Processing completed: {self._filled_count} successful, {failed_count} failed"
            )
            return results

        except Exception as e:
            if isinstance(e, FormFillerError):
                raise
            raise FormFillerError(f"Form processing failed: {e}")

    def validate_template(self, template_config: TemplateConfig) -> dict:
        """
        Validate template configuration and files.

        Args:
            template_config: Template configuration to validate

        Returns:
            Dictionary with validation results

        Raises:
            TemplateError: If template validation fails
        """
        try:
            results = {
                "template_exists": os.path.exists(template_config.template_path),
                "mapping_exists": os.path.exists(template_config.mapping_path),
                "template_path": template_config.template_path,
                "mapping_path": template_config.mapping_path,
            }

            if not results["template_exists"]:
                raise TemplateError(
                    f"Template file not found: {template_config.template_path}"
                )

            if not results["mapping_exists"]:
                raise TemplateError(
                    f"Mapping file not found: {template_config.mapping_path}"
                )

            # Try to load and validate mapping file
            try:
                mappings = self.data_processor.load_field_mappings(
                    template_config.mapping_path
                )
                results["mapping_fields_count"] = len(mappings)
                results["mapping_valid"] = True
            except Exception as e:
                raise TemplateError(f"Invalid mapping file: {e}")

            # Try to open and validate template PDF
            try:
                doc = fitz.open(template_config.template_path)
                results["template_pages"] = len(doc)
                results["template_valid"] = True
                doc.close()
            except Exception as e:
                raise TemplateError(f"Invalid template PDF: {e}")

            return results

        except Exception as e:
            if isinstance(e, TemplateError):
                raise
            raise TemplateError(f"Template validation failed: {e}")

    def get_processing_stats(self) -> dict:
        """
        Get current processing statistics.

        Returns:
            Dictionary with processing statistics
        """
        return {
            "filled_count": self._filled_count,
            "data_processor_stats": self.data_processor.get_mapping_summary(),
        }

    def reset(self) -> None:
        """Reset processing statistics and clear loaded data."""
        self._filled_count = 0
        self.data_processor = DataProcessor()
        logger.info("FormFiller reset completed")
