import os
import logging
from pythonjsonlogger import jsonlogger

def setup_logging():
    """
    Configures logging to output structured JSON.
    The log level is controlled by the LOG_LEVEL environment variable.
    """
    log_level = os.getenv('LOG_LEVEL', 'INFO').upper()

    logger = logging.getLogger()
    logger.setLevel(log_level)

    # Remove any existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    handler = logging.StreamHandler()

    # Format the logs as JSON
    formatter = jsonlogger.JsonFormatter(
        '%(asctime)s %(name)s %(levelname)s %(message)s'
    )

    handler.setFormatter(formatter)
    logger.addHandler(handler)
