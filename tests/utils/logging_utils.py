import inspect
import logging
from enum import Enum
from pathlib import Path

from framework.core.logger import get_logger


class LogClass(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


_LOG_LEVELS = {
    LogClass.INFO.value: logging.INFO,
    LogClass.WARNING.value: logging.WARNING,
    LogClass.ERROR.value: logging.ERROR,
}


def log(log_class: LogClass | str, text: str) -> None:
    level_name = _normalize_log_class(log_class)
    logger = get_logger("tests")
    caller = inspect.stack()[1]
    location = f"{Path(caller.filename).name}:{caller.lineno}"

    if level_name not in _LOG_LEVELS:
        logger.warning("[%s] Unsupported log class=%s. Original message: %s", location, log_class, text)
        return

    logger.log(_LOG_LEVELS[level_name], "[%s] %s", location, text)


def _normalize_log_class(log_class: LogClass | str) -> str:
    if isinstance(log_class, LogClass):
        return log_class.value

    return str(log_class).upper()
