"""Data processing utilities for FormFiller application."""

import csv
import logging
from typing import Any, Dict, List

import yaml

logger = logging.getLogger(__name__)


class DataProcessor:
    """Handles CSV data reading and field mapping operations."""

    def __init__(self):
        """Initialize the data processor."""
        self._field_mappings: Dict[str, Any] = {}
        self._csv_data: List[List[str]] = []

    def load_field_mappings(self, mapping_path: str) -> Dict[str, Any]:
        """
        Load field mappings from YAML file.

        Args:
            mapping_path: Path to the YAML mapping file

        Returns:
            Dictionary containing field mappings

        Raises:
            FileNotFoundError: If mapping file doesn't exist
            yaml.YAMLError: If YAML parsing fails
        """
        try:
            with open(mapping_path, "r", encoding="utf-8") as file:
                mappings = yaml.safe_load(file)
                if not isinstance(mappings, dict):
                    raise ValueError(f"Invalid mapping format in {mapping_path}")
                self._field_mappings = mappings
                logger.info(
                    f"Loaded {len(mappings)} field mappings from {mapping_path}"
                )
                return mappings
        except FileNotFoundError:
            logger.error(f"Mapping file not found: {mapping_path}")
            raise
        except yaml.YAMLError as e:
            logger.error(f"Error parsing YAML file {mapping_path}: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error loading mappings from {mapping_path}: {e}")
            raise

    def load_csv_data(self, csv_path: str) -> List[List[str]]:
        """
        Load CSV data from file.

        Args:
            csv_path: Path to the CSV file

        Returns:
            List of rows, where each row is a list of string values

        Raises:
            FileNotFoundError: If CSV file doesn't exist
            csv.Error: If CSV parsing fails
        """
        try:
            with open(csv_path, "r", encoding="utf-8") as file:
                reader = csv.reader(
                    file, quotechar='"', delimiter=",", quoting=csv.QUOTE_MINIMAL
                )
                data = list(reader)
                self._csv_data = data
                logger.info(f"Loaded {len(data)} rows from {csv_path}")
                return data
        except FileNotFoundError:
            logger.error(f"CSV file not found: {csv_path}")
            raise
        except csv.Error as e:
            logger.error(f"Error parsing CSV file {csv_path}: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error loading CSV from {csv_path}: {e}")
            raise

    def process_row(self, row: List[str], row_index: int) -> Dict[str, str]:
        """
        Process a single CSV row using field mappings.

        Args:
            row: List of string values from CSV row
            row_index: Index of the current row (for error reporting)

        Returns:
            Dictionary mapping PDF field names to values

        Raises:
            IndexError: If row doesn't have enough columns for mapping
            ValueError: If mapping configuration is invalid
        """
        if not self._field_mappings:
            raise ValueError(
                "Field mappings not loaded. Call load_field_mappings() first."
            )

        field_data = {}

        for field_name, csv_index in self._field_mappings.items():
            try:
                # Skip fields marked as unused
                if csv_index == "-1" or csv_index == -1:
                    continue

                if isinstance(csv_index, list):
                    # Multiple columns mapped to single field
                    values = []
                    for idx in csv_index:
                        if idx < len(row):
                            values.append(row[idx])
                        else:
                            logger.warning(
                                f"Column index {idx} out of range for row {row_index} "
                                f"(row length: {len(row)})"
                            )
                    field_data[field_name] = " \n".join(values)
                else:
                    # Single column mapped to field
                    if csv_index < len(row):
                        field_data[field_name] = row[csv_index]
                    else:
                        logger.warning(
                            f"Column index {csv_index} out of range for row {row_index} "
                            f"(row length: {len(row)})"
                        )
                        field_data[field_name] = ""

            except Exception as e:
                logger.error(
                    f"Error processing field '{field_name}' for row {row_index}: {e}"
                )
                field_data[field_name] = ""

        return field_data

    def process_all_data(self, skip_header: bool = False) -> List[Dict[str, str]]:
        """
        Process all loaded CSV data using field mappings.

        Args:
            skip_header: Whether to skip the first row

        Returns:
            List of dictionaries, each mapping PDF field names to values

        Raises:
            ValueError: If CSV data or field mappings not loaded
        """
        if not self._csv_data:
            raise ValueError("CSV data not loaded. Call load_csv_data() first.")

        if not self._field_mappings:
            raise ValueError(
                "Field mappings not loaded. Call load_field_mappings() first."
            )

        processed_data = []
        start_index = 1 if skip_header else 0

        for i, row in enumerate(self._csv_data[start_index:], start=start_index):
            # Skip empty rows
            if not row or all(not cell.strip() for cell in row):
                logger.debug(f"Skipping empty row {i}")
                continue

            try:
                field_data = self.process_row(row, i)
                processed_data.append(field_data)
            except Exception as e:
                logger.error(f"Failed to process row {i}: {e}")
                continue

        logger.info(f"Processed {len(processed_data)} rows successfully")
        return processed_data

    @property
    def field_mappings(self) -> Dict[str, Any]:
        """Get the loaded field mappings."""
        return self._field_mappings.copy()

    @property
    def csv_data(self) -> List[List[str]]:
        """Get the loaded CSV data."""
        return self._csv_data.copy()

    def get_mapping_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the loaded field mappings.

        Returns:
            Dictionary with mapping statistics
        """
        if not self._field_mappings:
            return {"total_fields": 0, "active_fields": 0, "unused_fields": 0}

        total_fields = len(self._field_mappings)
        unused_fields = sum(
            1 for val in self._field_mappings.values() if val == "-1" or val == -1
        )
        active_fields = total_fields - unused_fields

        return {
            "total_fields": total_fields,
            "active_fields": active_fields,
            "unused_fields": unused_fields,
            "multi_column_fields": sum(
                1 for val in self._field_mappings.values() if isinstance(val, list)
            ),
        }
