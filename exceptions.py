"""Custom exceptions for FormFiller application."""


class FormFillerError(Exception):
    """Base exception for FormFiller application."""

    pass


class ConfigurationError(FormFillerError):
    """Raised when there's an error in configuration."""

    pass


class DataProcessingError(FormFillerError):
    """Raised when there's an error processing CSV data."""

    pass


class TemplateError(FormFillerError):
    """Raised when there's an error with PDF templates."""

    pass


class ValidationError(FormFillerError):
    """Raised when validation fails."""

    pass


class FileNotFoundError(FormFillerError):
    """Raised when a required file is not found."""

    pass
