from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from framework.core.browser import Browser
from framework.utils.waiter import Locator, Waiter


class BaseElement:
    def __init__(self, locator: Locator, name: str) -> None:
        self.locator = locator
        self.name = name

    def find_element(self) -> WebElement:
        return Waiter.visible(self.locator)

    def find_present_element(self) -> WebElement:
        return Waiter.present(self.locator)

    def find_clickable_element(self) -> WebElement:
        return Waiter.clickable(self.locator)

    def find_elements(self) -> list[WebElement]:
        return Browser().driver.find_elements(*self.locator)

    def click(self) -> None:
        def _click(driver: WebDriver) -> bool:
            try:
                for element in driver.find_elements(*self.locator):
                    if element.is_displayed() and element.is_enabled():
                        element.click()
                        return True
            except StaleElementReferenceException:
                return False
            return False

        Waiter.until(_click)

    def text(self) -> str:
        return self.find_element().text

    def get_attribute(self, attribute_name: str) -> str | None:
        return self.find_element().get_attribute(attribute_name)

    def is_displayed(self) -> bool:
        return Waiter.is_visible(self.locator)
