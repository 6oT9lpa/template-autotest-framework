from selenium.webdriver.remote.webdriver import WebDriver

from framework.core.browser_factories import BrowserFactory
from framework.core.log_messages import InfoMessages
from framework.core.logger import get_logger
from framework.core.settings import ConfigManager
from framework.core.singleton import SingletonMeta

logger = get_logger(__name__)


class Browser(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self._driver: WebDriver | None = None

    @property
    def driver(self) -> WebDriver:
        if self._driver is None:
            config = ConfigManager().config
            logger.info(InfoMessages.DRIVER_CREATE.format(browser=config.browser, incognito=config.incognito))
            self._driver = BrowserFactory.create_driver(config)
            self._driver.implicitly_wait(config.implicit_wait)
            self._driver.maximize_window()
            logger.info(InfoMessages.DRIVER_READY)
        return self._driver

    def get_driver(self) -> WebDriver:
        return self.driver

    def open(self, url: str) -> None:
        logger.info(InfoMessages.OPEN_URL.format(url=url))
        self.driver.get(url)

    def quit(self) -> None:
        if self._driver is not None:
            self._driver.quit()
            self._driver = None
            logger.info(InfoMessages.DRIVER_QUIT)
