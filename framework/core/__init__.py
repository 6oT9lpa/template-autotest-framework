__all__ = [
    "Browser",
    "ConfigManager",
    "ErrorMessages",
    "InfoMessages",
    "LoggerManager",
    "SingletonMeta",
    "TestDataManager",
    "WarningMessages",
    "get_logger",
]


def __getattr__(name: str):
    if name == "Browser":
        from framework.core.browser import Browser

        return Browser

    if name in {"ErrorMessages", "InfoMessages", "WarningMessages"}:
        from framework.core.log_messages import ErrorMessages, InfoMessages, WarningMessages

        return {
            "ErrorMessages": ErrorMessages,
            "InfoMessages": InfoMessages,
            "WarningMessages": WarningMessages,
        }[name]

    if name in {"LoggerManager", "get_logger"}:
        from framework.core.logger import LoggerManager, get_logger

        return {
            "LoggerManager": LoggerManager,
            "get_logger": get_logger,
        }[name]

    if name in {"ConfigManager", "TestDataManager"}:
        from framework.core.settings import ConfigManager, TestDataManager

        return {
            "ConfigManager": ConfigManager,
            "TestDataManager": TestDataManager,
        }[name]

    if name == "SingletonMeta":
        from framework.core.singleton import SingletonMeta

        return SingletonMeta

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
