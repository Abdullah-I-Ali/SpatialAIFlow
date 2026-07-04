"""
Centralized logging for the SpatialAIFlow framework.
"""
import logging
import sys

def get_logger(name: str = "spatialaiflow") -> logging.Logger:
    """
    Get a configured logger for the framework.

    Parameters
    ----------
    name : str, optional
        The name of the logger, by default "spatialaiflow".

    Returns
    -------
    logging.Logger
        Configured logger instance.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.propagate = False
    return logger

logger = get_logger()
