import logging
from logging.config import dictConfig
from pathlib import Path

from framework.core.settings import ConfigManager
from framework.core.singleton import SingletonMeta


class LoggerManager(metaclass=SingletonMeta):
    LOGGER_NAMES = ("framework", "tests")

    def __init__(self) -> None:
        self._configure()

    def get_logger(self, name: str) -> logging.Logger:
        return logging.getLogger(name)

    def _configure(self) -> None:
        config = ConfigManager().config.logging
        logging.disable(logging.NOTSET)

        if not config.enabled:
            logging.disable(logging.CRITICAL)

        handlers = {}
        active_handlers = []

        if config.console_enabled:
            handlers["console"] = {
                "class": "logging.StreamHandler",
                "level": config.level,
                "formatter": "default",
            }
            active_handlers.append("console")

        if config.file_enabled:
            log_file_path = self._resolve_log_path(config.file_path)
            log_file_path.parent.mkdir(parents=True, exist_ok=True)
            handlers["file"] = {
                "class": "logging.handlers.RotatingFileHandler",
                "level": config.level,
                "formatter": "default",
                "filename": str(log_file_path),
                "maxBytes": config.max_bytes,
                "backupCount": config.backup_count,
                "encoding": "utf-8",
            }
            active_handlers.append("file")

        dictConfig(
            {
                "version": 1,
                "disable_existing_loggers": False,
                "formatters": {
                    "default": {
                        "format": config.format,
                        "datefmt": config.date_format,
                    }
                },
                "handlers": handlers,
                "loggers": {
                    logger_name: {
                        "level": config.level,
                        "handlers": active_handlers,
                        "propagate": False,
                    }
                    for logger_name in self.LOGGER_NAMES
                },
            }
        )

    @staticmethod
    def _resolve_log_path(file_path: str) -> Path:
        path = Path(file_path)
        if path.is_absolute():
            return path

        return Path(__file__).resolve().parents[2] / path


def get_logger(name: str) -> logging.Logger:
    return LoggerManager().get_logger(name)
