from selenium.webdriver.common.keys import Keys

from framework.elements.base_element import BaseElement


class Input(BaseElement):
    def type(self, text: str) -> None:
        self.find_element().send_keys(text)

    def clear(self) -> None:
        self.find_element().clear()

    def clear_and_type(self, text: str) -> None:
        element = self.find_element()
        element.clear()
        element.send_keys(text)

    def press_enter(self) -> None:
        self.find_element().send_keys(Keys.ENTER)
