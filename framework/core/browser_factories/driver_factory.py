from abc import ABC, abstractmethod

from selenium.webdriver.common.options import ArgOptions
from selenium.webdriver.remote.webdriver import WebDriver

from framework.models.config import Config


class DriverFactory(ABC):
    @abstractmethod
    def create(self, config: Config) -> WebDriver:
        pass

    def _add_browser_arguments(self, options: ArgOptions, config: Config) -> None:
        for argument in config.browser_arguments:
            options.add_argument(argument)
