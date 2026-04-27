import logging
import sys


def setup_logger(name: str) -> logging.Logger:
    """
    Creates and configures a centralized logger for the application.

    Args:
        name: The name of the module/logger.

    Returns:
        A configured logging.Logger instance.
    """
    logger = logging.getLogger(name)

    logger.setLevel(logging.INFO)

    # Prevent adding multiple handlers
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)

        # Format: timestamp - logger name - level - message
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)

        logger.addHandler(handler)

    return logger
