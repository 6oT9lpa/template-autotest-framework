from abc import ABC, abstractmethod
from typing import Callable

from selenium.common.exceptions import ElementClickInterceptedException, StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from framework.core.browser import Browser
from framework.core.logger import get_logger
from framework.utils.waiter import Locator, Waiter
from framework.utils.js_actions import JsActions

logger = get_logger(__name__)


class BaseElement(ABC):
    def __init__(self, locator: Locator, name: str) -> None:
        self._locator = locator
        self._name = name

    @property
    @abstractmethod
    def element_type(self) -> str:
        pass

    @property
    def name(self) -> str:
        return self._name

    def _find_element(self, should_log: bool = True) -> WebElement:
        return self._find_with_log(
            condition="visible",
            finder=Waiter.visible,
            should_log=should_log,
        )

    def _find_present_element(self, should_log: bool = True) -> WebElement:
        return self._find_with_log(
            condition="present",
            finder=Waiter.present,
            should_log=should_log,
        )

    def _find_clickable_element(self, should_log: bool = True) -> WebElement:
        return self._find_with_log(
            condition="clickable",
            finder=Waiter.clickable,
            should_log=should_log,
        )

    def click(self) -> None:
        logger.info("[%s] Clicking element: name='%s', locator=%s", self.element_type, self.name, self._locator)

        def _try_click(driver: WebDriver) -> bool:
            try:
                element = driver.find_element(*self._locator)
                if element.is_displayed() and element.is_enabled():
                    element.click()
                    return True

            except ElementClickInterceptedException:
                logger.warning(
                    "[%s] Element click intercepted: name='%s', locator=%s",
                    self.element_type,
                    self.name,
                    self._locator,
                )
                return False

            except StaleElementReferenceException:
                logger.warning(
                    "[%s] Stale element while clicking: name='%s', locator=%s",
                    self.element_type,
                    self.name,
                    self._locator,
                )
                return False

            return False

        Waiter.until(_try_click)
        logger.info("[%s] Element clicked: name='%s', locator=%s", self.element_type, self.name, self._locator)

    def click_by_js(self) -> None:
        element = self._find_element()
        logger.info("[%s] Scrolling element into view: name='%s', locator=%s", self.element_type, self.name, self._locator)

        JsActions.scroll_into_view(element)
        logger.info("[%s] Clicking element via JavaScript: name='%s', locator=%s", self.element_type, self.name, self._locator)

        JsActions.click(element)
        logger.info("[%s] Element clicked via JavaScript: name='%s', locator=%s", self.element_type, self.name, self._locator)

    def text(self) -> str:
        text = self._find_element().text
        logger.info(
            "[%s] Element text received: name='%s', locator=%s, text='%s'",
            self.element_type,
            self.name,
            self._locator,
            text,
        )
        return text

    def get_attribute(self, attribute_name: str, should_log: bool = True) -> str | None:
        value = self._find_element(should_log=should_log).get_attribute(attribute_name)
        if should_log:
            logger.info(
                "[%s] Element attribute received: name='%s', locator=%s, attribute='%s', value='%s'",
                self.element_type,
                self.name,
                self._locator,
                attribute_name,
                value,
            )
        return value

    def get_present_attribute(self, attribute_name: str, should_log: bool = True) -> str | None:
        value = self._find_present_element(should_log=should_log).get_attribute(attribute_name)
        if should_log:
            logger.info(
                "[%s] Element attribute received: name='%s', locator=%s, attribute='%s', value='%s'",
                self.element_type,
                self.name,
                self._locator,
                attribute_name,
                value,
            )
        return value

    def is_displayed(self, timeout: int | None = None) -> bool:
        displayed = Waiter.is_visible(self._locator, timeout)
        logger.info(
            "[%s] Element displayed check: name='%s', locator=%s, displayed=%s",
            self.element_type,
            self.name,
            self._locator,
            displayed,
        )
        return displayed

    def click_at_center(self, should_log: bool = True) -> None:
        element = self._find_element(should_log=should_log)

        ActionChains(Browser().get_driver()) \
            .move_to_element(element) \
            .click() \
            .perform()

        if should_log:
            logger.info("[%s] Element clicked at center: name='%s', locator=%s", self.element_type, self.name, self._locator)

    def send_keys(self, *keys: str, should_log: bool = True) -> None:
        self._find_element(should_log=should_log).send_keys(*keys)

    def send_keys_when_present(self, *keys: str, should_log: bool = True) -> None:
        self._find_present_element(should_log=should_log).send_keys(*keys)

    def width(self, should_log: bool = True) -> int:
        return self._find_element(should_log=should_log).size["width"]

    def drag_by_offset_from_center(self, current_x: int, target_x: int, should_log: bool = True) -> None:
        element = self._find_element(should_log=should_log)
        ActionChains(Browser().get_driver()).move_to_element_with_offset(element, current_x, 0).click_and_hold().move_by_offset(
            target_x - current_x,
            0,
        ).release().perform()

    def _find_with_log(
        self,
        condition: str,
        finder: Callable[[Locator], WebElement],
        should_log: bool = True,
    ) -> WebElement:
        if should_log:
            logger.info(
                "[%s] Searching element: name='%s', locator=%s, condition='%s'",
                self.element_type,
                self.name,
                self._locator,
                condition,
            )

        element = finder(self._locator)

        if should_log:
            logger.info(
                "[%s] Element found: name='%s', locator=%s, condition='%s'",
                self.element_type,
                self.name,
                self._locator,
                condition,
            )

        return element
