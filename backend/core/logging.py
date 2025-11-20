import logging
import sys
from backend.core.config import get_settings

settings = get_settings()

def setup_logging():
    logger = logging.getLogger(settings.APP_NAME)
    logger.setLevel(settings.LOG_LEVEL)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    
    if not logger.handlers:
        logger.addHandler(console_handler)
    
    return logger

logger = setup_logging()
