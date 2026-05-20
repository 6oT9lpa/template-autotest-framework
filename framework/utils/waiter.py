from collections.abc import Callable
from typing import Any

from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from framework.core.browser import Browser
from framework.core.logger import get_logger
from framework.core.settings import ConfigManager

Locator = tuple[str, str]
logger = get_logger(__name__)


class Waiter:
    @staticmethod
    def until(condition: Callable[[WebDriver], Any], timeout: int | None = None) -> Any:
        wait_timeout = timeout if timeout is not None else ConfigManager().config.explicit_wait
        try:
            return WebDriverWait(Browser().get_driver(), wait_timeout).until(condition)
        except TimeoutException:
            logger.error("Timeout while waiting for condition: timeout=%s", wait_timeout)
            raise

    @staticmethod
    def visible(locator: Locator, timeout: int | None = None) -> Any:
        def _visible(driver: WebDriver) -> Any:
            try:
                for element in driver.find_elements(*locator):
                    if element.is_displayed():
                        return element
            except StaleElementReferenceException:
                logger.warning("Stale element while waiting for locator=%s", locator)
                return False
            return False

        return Waiter.until(_visible, timeout)

    @staticmethod
    def clickable(locator: Locator, timeout: int | None = None) -> Any:
        def _clickable(driver: WebDriver) -> Any:
            try:
                for element in driver.find_elements(*locator):
                    if element.is_displayed() and element.is_enabled():
                        return element
            except StaleElementReferenceException:
                logger.warning("Stale element while waiting for locator=%s", locator)
                return False
            return False

        return Waiter.until(_clickable, timeout)

    @staticmethod
    def present(locator: Locator, timeout: int | None = None) -> Any:
        return Waiter.until(EC.presence_of_element_located(locator), timeout)

    @staticmethod
    def is_visible(locator: Locator, timeout: int | None = None) -> bool:
        try:
            Waiter.visible(locator, timeout)
            return True
        except TimeoutException:
            wait_timeout = timeout if timeout is not None else ConfigManager().config.explicit_wait
            logger.error("Element was not visible: locator=%s, timeout=%s", locator, wait_timeout)
            return False
