from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.remote.webdriver import WebDriver

from framework.core.browser_factories.driver_factory import DriverFactory
from framework.models.config import Config


class ChromeDriverFactory(DriverFactory):
    INCOGNITO_ARGUMENT = "--incognito"

    def create(self, config: Config) -> WebDriver:
        options = ChromeOptions()
        if config.incognito:
            options.add_argument(self.INCOGNITO_ARGUMENT)
        self._add_browser_arguments(options, config)
        return webdriver.Chrome(options=options)
