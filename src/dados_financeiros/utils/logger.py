import sys

from loguru import logger

LOG_FORMAT = "{time:YYYY-MM-DD HH:mm:ss} - {name} - {level} - {message}"

logger.remove()
logger.add(sys.stdout, format=LOG_FORMAT, level="INFO")
logger.add(".log", format=LOG_FORMAT, level="INFO", rotation="10 MB", retention="10 days", encoding="utf-8")
