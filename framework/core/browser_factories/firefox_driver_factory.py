from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.remote.webdriver import WebDriver

from framework.core.browser_factories.driver_factory import DriverFactory
from framework.models.config import Config


class FirefoxDriverFactory(DriverFactory):
    INCOGNITO_ARGUMENT = "-private"

    def create(self, config: Config) -> WebDriver:
        options = FirefoxOptions()
        if config.incognito:
            options.add_argument(self.INCOGNITO_ARGUMENT)
        self._add_browser_arguments(options, config)
        return webdriver.Firefox(options=options)
