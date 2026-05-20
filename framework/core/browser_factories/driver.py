from abc import ABC, abstractmethod
from typing import Any

from selenium.webdriver.common.options import ArgOptions
from selenium.webdriver.remote.webdriver import WebDriver

from framework.models.browser_config import BrowserConfig
from framework.models.config import Config
from framework.utils.download import DownloadUtils


class DriverFactory(ABC):
    DOWNLOAD_DIR_PLACEHOLDER = "{download_dir}"

    @abstractmethod
    def create(self, config: Config, browser_config: BrowserConfig) -> WebDriver:
        pass

    def _add_browser_arguments(self, options: ArgOptions, browser_config: BrowserConfig) -> None:
        for argument in browser_config.arguments:
            options.add_argument(argument)

    def _resolve_config_value(self, value: Any) -> Any:
        if isinstance(value, str):
            return value.replace(
                self.DOWNLOAD_DIR_PLACEHOLDER,
                str(DownloadUtils.directory()),
            )

        if isinstance(value, dict):
            return {
                key: self._resolve_config_value(nested_value)
                for key, nested_value in value.items()
            }

        if isinstance(value, list):
            return [
                self._resolve_config_value(nested_value)
                for nested_value in value
            ]

        if isinstance(value, tuple):
            return tuple(
                self._resolve_config_value(nested_value)
                for nested_value in value
            )

        return value
