from selenium import webdriver
from selenium.webdriver import EdgeOptions
from selenium.webdriver.remote.webdriver import WebDriver

from framework.core.browser_factories.driver_factory import DriverFactory
from framework.models.config import Config


class EdgeDriverFactory(DriverFactory):
    INCOGNITO_ARGUMENT = "--inprivate"

    def create(self, config: Config) -> WebDriver:
        options = EdgeOptions()
        if config.incognito:
            options.add_argument(self.INCOGNITO_ARGUMENT)
        self._add_browser_arguments(options, config)
        return webdriver.Edge(options=options)
