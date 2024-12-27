"""
Logger configuration for the application
"""

import logging
from src.utils.constants import LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)
logger.setLevel(logging.INFO)

if not logger.handlers:
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
                                datefmt='%Y-%m-%d %H:%M:%S')

    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

logger.propagate = False 