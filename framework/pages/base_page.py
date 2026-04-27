from abc import ABC, abstractmethod

from selenium.webdriver.remote.webdriver import WebDriver

from framework.core.browser import Browser
from framework.elements.base_element import BaseElement


class BasePage(ABC):
    @property
    @abstractmethod
    def unique_element(self) -> BaseElement:
        raise NotImplementedError("Page object must define a unique page element.")

    @property
    def driver(self) -> WebDriver:
        return Browser().driver

    def is_opened(self) -> bool:
        return self.unique_element.is_displayed()
