from selenium.webdriver.remote.webdriver import WebDriver

from framework.core.browser_factories.chrome_driver import ChromeDriverFactory
from framework.core.browser_factories.driver import DriverFactory
from framework.core.browser_factories.edge_driver import EdgeDriverFactory
from framework.core.browser_factories.firefox_driver import FirefoxDriverFactory
from framework.core.logger import get_logger
from framework.models.browser_config import BrowserConfig
from framework.models.config import Config

logger = get_logger(__name__)


class BrowserFactory:
    _factories: dict[str, DriverFactory] = {
        "chrome": ChromeDriverFactory(),
        "edge": EdgeDriverFactory(),
        "firefox": FirefoxDriverFactory(),
    }

    @classmethod
    def create_driver(cls, config: Config, browser_config: BrowserConfig) -> WebDriver:
        browser_name = config.browser.lower()
        if browser_name not in cls._factories:
            logger.error("Unsupported browser requested: %s", config.browser)
            raise ValueError(f"Unsupported browser: {config.browser}")
        return cls._factories[browser_name].create(config, browser_config)
