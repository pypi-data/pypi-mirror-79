__version__ = "6.1.4"

import logging

logging.basicConfig()
logger = logging.getLogger("zuper-commons")
logger.setLevel(logging.DEBUG)

logger.info(f"commons {__version__}")
