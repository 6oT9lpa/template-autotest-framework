from abc import ABC, abstractmethod

from selenium import webdriver
from selenium.webdriver import ChromeOptions, EdgeOptions
from selenium.webdriver.remote.webdriver import WebDriver

from framework.core.log_messages import ErrorMessages
from framework.core.logger import get_logger
from framework.models.config import Config

logger = get_logger(__name__)

class DriverFactory(ABC):
    @abstractmethod
    def create(self, config: Config) -> WebDriver:
        pass

class ChromeDriverFactory(DriverFactory):
    INCOGNITO_ARGUMENT = "--incognito"

    def create(self, config: Config) -> WebDriver:
        options = ChromeOptions()
        if config.incognito:
            options.add_argument(self.INCOGNITO_ARGUMENT)
        for argument in config.browser_arguments:
            options.add_argument(argument)
        return webdriver.Chrome(options=options)


class EdgeDriverFactory(DriverFactory):
    INCOGNITO_ARGUMENT = "--inprivate"

    def create(self, config: Config) -> WebDriver:
        options = EdgeOptions()
        if config.incognito:
            options.add_argument(self.INCOGNITO_ARGUMENT)
        for argument in config.browser_arguments:
            options.add_argument(argument)
        return webdriver.Edge(options=options)


class BrowserFactory:
    _factories: dict[str, DriverFactory] = {
        "chrome": ChromeDriverFactory(),
        "edge": EdgeDriverFactory(),
    }

    @classmethod
    def create_driver(cls, config: Config) -> WebDriver:
        browser_name = config.browser.lower()
        if browser_name not in cls._factories:
            logger.error(ErrorMessages.UNSUPPORTED_BROWSER.format(browser=config.browser))
            raise ValueError(f"Unsupported browser: {config.browser}")
        return cls._factories[browser_name].create(config)
