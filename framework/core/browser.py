from selenium.webdriver.remote.webdriver import WebDriver

from framework.core.browser_factories import BrowserFactory
from framework.core.logger import get_logger
from framework.core.settings import ConfigManager
from framework.core.singleton import SingletonMeta

logger = get_logger(__name__)


class Browser(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self._driver: WebDriver | None = None

    def get_driver(self) -> WebDriver:
        if self._driver is None:
            config_manager = ConfigManager()
            config = config_manager.config
            browser_config = config_manager.browser_config

            logger.info(
                "Creating browser driver: browser=%s, incognito=%s",
                config.browser,
                browser_config.incognito,
            )

            self._driver = BrowserFactory.create_driver(config, browser_config)
            self._driver.implicitly_wait(config.implicit_wait)
            self._driver.maximize_window()

            logger.info("Browser driver is ready")

        return self._driver

    def open(self, url: str) -> None:
        logger.info("Opening URL: %s", url)
        self.get_driver().get(url)

    def quit(self) -> None:
        if self._driver is not None:
            self._driver.quit()
            self._driver = None

            logger.info("Browser driver was closed")
