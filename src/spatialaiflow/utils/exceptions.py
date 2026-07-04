"""
Custom exceptions for the SpatialAIFlow framework.
"""

class SpatialAIFlowError(Exception):
    """Base exception for all SpatialAIFlow errors."""
    pass


class DataValidationError(SpatialAIFlowError):
    """Raised when an AnnData object fails validation checks."""
    pass


class ModelExecutionError(SpatialAIFlowError):
    """Raised when an external model or algorithm fails to execute."""
    pass


class ConfigurationError(SpatialAIFlowError):
    """Raised when invalid configuration or parameters are provided."""
    pass
