import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional


class SingletonLogger:
    _instances = {}

    def __new__(cls, name: str, log_level: int = logging.INFO, log_dir: Optional[Path] = None, log_file: str = "app.log"):
        # If an instance for this logger name already exists, return it
        if name in cls._instances:
            return cls._instances[name]

        # Otherwise, create a new instance
        instance = super().__new__(cls)
        cls._instances[name] = instance
        return instance

    def __init__(self, name: str, log_level: int = logging.INFO, log_dir: Optional[Path] = None, log_file: str = "app.log"):
        # Avoid re-initializing if already initialized
        if hasattr(self, "_initialized") and self._initialized:
            return

        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)
        self.logger.propagate = False

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
        self.logger.addHandler(console_handler)

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
                self.logger.addHandler(file_handler)
            except Exception as e:
                self.logger.error(f"Failed to initialize file logger: {e}")

        self._initialized = True

    def get_logger(self) -> logging.Logger:
        return self.logger
