import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional


def get_logger(
    name: str,
    log_level: int = logging.INFO,
    log_dir: Optional[Path] = None,
    log_file: str = "app.log",
) -> logging.Logger:
    """
    Create and return a configured logger.

    Args:
        name (str): Logger name (usually __name__)
        log_level (int): Logging level (INFO, DEBUG, ERROR, etc.)
        log_dir (Path | None): Directory to store log files
        log_file (str): Log file name

    Returns:
        logging.Logger: Configured logger instance
    """

    logger = logging.getLogger(name)

    # Prevent duplicate logs
    if logger.handlers:
        return logger

    logger.setLevel(log_level)
    logger.propagate = False

    # -------------------------
    # Log format
    # -------------------------
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(filename)s:%(lineno)d | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # -------------------------
    # Console handler
    # -------------------------
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # -------------------------
    # File handler (optional)
    # -------------------------
    if log_dir:
        try:
            log_dir.mkdir(parents=True, exist_ok=True)
            file_handler = RotatingFileHandler(
                filename=log_dir / log_file,
                maxBytes=5 * 1024 * 1024,  # 5 MB
                backupCount=5,
                encoding="utf-8",
            )
            file_handler.setLevel(log_level)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except Exception as e:
            logger.error(f"Failed to initialize file logger: {e}")

    return logger
