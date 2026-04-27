import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from framework.core.browser import Browser


@pytest.fixture
def browser():
    browser_instance = Browser()
    driver = browser_instance.get_driver()
    yield driver
    browser_instance.quit()


