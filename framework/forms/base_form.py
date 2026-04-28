from abc import ABC, abstractmethod

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait

from framework.core.browser import Browser
from framework.elements.base_element import BaseElement


class BaseForm(ABC):
    @property
    @abstractmethod
    def unique_element(self) -> BaseElement:
        raise NotImplementedError("Form object must define a unique form element.")

    @property
    def driver(self) -> WebDriver:
        return Browser().driver

    def is_opened(self) -> bool:
        return self.unique_element.is_displayed()

    def is_closed(self) -> bool:
        elements = self.driver.find_elements(*self.unique_element.locator)
        return not any(element.is_displayed() for element in elements)

    def wait_until_closed(self, timeout: int = 2) -> bool:
        try:
            return WebDriverWait(self.driver, timeout).until(lambda _driver: self.is_closed())
        except TimeoutException:
            return False
