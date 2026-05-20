from abc import ABC, abstractmethod

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

from framework.core.browser import Browser
from framework.core.logger import get_logger
from framework.elements import ElementFactory
from framework.utils.waiter import Locator

logger = get_logger(__name__)


class BasePage(ABC):
    @abstractmethod
    def __init__(self, unique_element_locator: Locator, name: str) -> None:
        self._name = name
        self._unique_element = ElementFactory.text(unique_element_locator, f"{name} unique element")

    @property
    def name(self) -> str:
        return self._name

    def is_opened(self, timeout: int | None = None) -> bool:
        logger.info("Checking '%s' is opened through unique element '%s'", self.name, self._unique_element.name)
        opened = self._unique_element.is_displayed(timeout)
        logger.info("Object opened check result: object='%s', opened=%s", self.name, opened)
        return opened

    def is_closed(self, timeout: int = 0) -> bool:
        logger.info("Checking '%s' is closed through unique element '%s'", self.name, self._unique_element.name)
        closed = not self.is_opened(timeout)
        logger.info("Object closed check result: object='%s', closed=%s", self.name, closed)
        return closed

    def wait_until_closed(self, timeout: int = 2) -> bool:
        logger.info("Waiting until '%s' is closed: timeout=%s", self.name, timeout)
        try:
            closed = WebDriverWait(Browser().get_driver(), timeout).until(lambda _driver: self.is_closed())
            logger.info("Object closed wait result: object='%s', closed=%s", self.name, closed)
            return closed
        except TimeoutException:
            logger.warning("Object is still opened after waiting: object='%s', timeout=%s", self.name, timeout)
            return False
