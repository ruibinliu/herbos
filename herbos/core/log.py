import logging

from pathlib import Path

from logging.handlers import RotatingFileHandler


LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

logger = logging.getLogger("herbos")
logger.setLevel(logging.INFO)
logger.propagate = False


formatter = logging.Formatter(
    "[%(asctime)s] "
    "[%(levelname)s] "
    "%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

file_handler = RotatingFileHandler(
    LOG_DIR / "app.log",
    maxBytes=1 * 1024 * 1024,  # 1 MB
    backupCount=5,
    encoding="utf-8"
)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
