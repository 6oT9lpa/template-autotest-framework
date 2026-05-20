from selenium.webdriver.support import expected_conditions as EC

from framework.core.logger import get_logger
from framework.utils.waiter import Waiter

logger = get_logger(__name__)


class AlertUtils:
    @staticmethod
    def text(timeout: int | float | None = None) -> str:
        logger.info("Waiting for alert: timeout=%s", timeout)
        text = Waiter.until(EC.alert_is_present(), timeout=timeout).text
        logger.info("Alert text received: text='%s'", text)
        return text

    @staticmethod
    def accept() -> None:
        logger.info("Accepting alert")
        Waiter.until(EC.alert_is_present()).accept()
        logger.info("Alert accepted")

    @staticmethod
    def type_text_and_accept(text: str) -> None:
        logger.info("Typing text into prompt alert and accepting: text='%s'", text)
        alert = Waiter.until(EC.alert_is_present())
        alert.send_keys(text)
        alert.accept()
        logger.info("Alert accepted")
