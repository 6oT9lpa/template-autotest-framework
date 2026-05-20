from selenium.webdriver.common.keys import Keys

from framework.core.logger import get_logger
from framework.elements.base_element import BaseElement

logger = get_logger(__name__)


class Input(BaseElement):
    @property
    def element_type(self) -> str:
        return "input"

    def type(self, text: str) -> None:
        logger.info("Typing text into input: name='%s', locator=%s, text='%s'", self.name, self._locator, text)
        self.send_keys(text)

    def type_when_present(self, text: str) -> None:
        logger.info("Typing text into input: name='%s', locator=%s, text='%s'", self.name, self._locator, text)
        self.send_keys_when_present(text)

    def clear(self) -> None:
        logger.info("Clearing input: name='%s', locator=%s", self.name, self._locator)
        self._find_element().clear()

    def clear_and_type(self, text: str) -> None:
        logger.info("Clearing input and typing text: name='%s', locator=%s, text='%s'", self.name, self._locator, text)
        element = self._find_element()
        element.clear()
        element.send_keys(text)

    def press_enter(self) -> None:
        logger.info("Pressing Enter in input: name='%s', locator=%s", self.name, self._locator)
        self.send_keys(Keys.ENTER)
