__version__ = "6.1.5"

import logging

logging.basicConfig()
logger = logging.getLogger("commons")
logger.setLevel(logging.DEBUG)

logger.info(f"version: {__version__}")
