import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filemode="w",
    filename=".log",
    encoding="utf-8",
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
