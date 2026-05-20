from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.remote.webdriver import WebDriver

from framework.core.browser_factories.driver import DriverFactory
from framework.models.browser_config import BrowserConfig
from framework.models.config import Config


class FirefoxDriverFactory(DriverFactory):
    INCOGNITO_ARGUMENT = "-private"

    def create(self, config: Config, browser_config: BrowserConfig) -> WebDriver:
        options = FirefoxOptions()
        for name, value in browser_config.firefox.preferences.items():
            options.set_preference(name, self._resolve_config_value(value))
        if browser_config.incognito:
            options.add_argument(self.INCOGNITO_ARGUMENT)
        self._add_browser_arguments(options, browser_config)
        return webdriver.Firefox(options=options)
