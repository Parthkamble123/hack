# utils/logger.py

import logging
import os

def get_logger(name: str) -> logging.Logger:
    """
    Returns a named logger.
    All modules should use: from utils.logger import get_logger
    """
    os.makedirs("logs", exist_ok=True)
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        ))
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger
