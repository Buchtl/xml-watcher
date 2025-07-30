import sys
import os
import pathlib
import logging
from logging.handlers import TimedRotatingFileHandler

def config():
    log_level_str = os.getenv("LOG_LEVEL", "INFO").upper()
    log_dir = pathlib.Path(os.getenv("LOG_DIR", "logs"))
    log_level = getattr(
        logging, log_level_str, logging.INFO
    )  # defaults to INFO if invalid
    os.makedirs(log_dir.as_posix(), exist_ok=True)

    # Log Format
    log_format = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    formatter = logging.Formatter(log_format)
    # Logger setup
    logger = logging.getLogger("xml_watcher")
    logger.setLevel(log_level)
    # File handler: one file per day, keep 7 days
    file_handler = TimedRotatingFileHandler(
        filename=(log_dir / "app.log").as_posix(),
        when="midnight",
        interval=1,
        backupCount=7,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    # Stdout handler
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(formatter)
    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(stdout_handler)
    logger.info(f"Start logging (LOG_DIR: {log_dir.absolute()})")