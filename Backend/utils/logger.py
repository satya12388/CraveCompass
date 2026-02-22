import logging
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "menu_ai.log"

def setup_logger():
    logger = logging.getLogger("menu_ai")
    logger.setLevel(logging.INFO)

    handler = logging.FileHandler(LOG_FILE, encoding="utf-8")

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(handler)

    return logger


logger = setup_logger()