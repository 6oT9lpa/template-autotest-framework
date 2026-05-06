from selenium.webdriver.remote.webdriver import WebDriver

from framework.core.browser_factories.chrome_driver_factory import ChromeDriverFactory
from framework.core.browser_factories.driver_factory import DriverFactory
from framework.core.browser_factories.edge_driver_factory import EdgeDriverFactory
from framework.core.browser_factories.firefox_driver_factory import FirefoxDriverFactory
from framework.core.log_messages import ErrorMessages
from framework.core.logger import get_logger
from framework.models.config import Config

logger = get_logger(__name__)


class BrowserFactory:
    _factories: dict[str, DriverFactory] = {
        "chrome": ChromeDriverFactory(),
        "edge": EdgeDriverFactory(),
        "firefox": FirefoxDriverFactory(),
    }

    @classmethod
    def create_driver(cls, config: Config) -> WebDriver:
        browser_name = config.browser.lower()
        if browser_name not in cls._factories:
            logger.error(ErrorMessages.UNSUPPORTED_BROWSER.format(browser=config.browser))
            raise ValueError(f"Unsupported browser: {config.browser}")
        return cls._factories[browser_name].create(config)
