from selenium.webdriver.remote.webelement import WebElement

from framework.core.browser import Browser
from framework.core.log_messages import InfoMessages
from framework.core.logger import get_logger

logger = get_logger(__name__)


class JsActions:
    @staticmethod
    def click(element: WebElement) -> None:
        logger.info(InfoMessages.JS_CLICK.format(element=element))
        Browser().driver.execute_script("arguments[0].click();", element)
