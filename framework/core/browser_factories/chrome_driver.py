from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.remote.webdriver import WebDriver

from framework.core.browser_factories.driver import DriverFactory
from framework.models.browser_config import BrowserConfig
from framework.models.config import Config


class ChromeDriverFactory(DriverFactory):
    INCOGNITO_ARGUMENT = "--incognito"

    def create(self, config: Config, browser_config: BrowserConfig) -> WebDriver:
        options = ChromeOptions()
        for name, value in browser_config.chromium.experimental_options.items():
            options.add_experimental_option(name, self._resolve_config_value(value))
        if browser_config.incognito:
            options.add_argument(self.INCOGNITO_ARGUMENT)
        self._add_browser_arguments(options, browser_config)
        driver = webdriver.Chrome(options=options)
        for command in browser_config.chromium.cdp_commands:
            driver.execute_cdp_cmd(command.name, self._resolve_config_value(command.params))
        return driver
