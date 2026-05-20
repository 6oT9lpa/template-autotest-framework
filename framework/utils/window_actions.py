from selenium.webdriver.remote.webdriver import WebDriver

from framework.core.browser import Browser
from framework.core.logger import get_logger
from framework.utils.waiter import Waiter

logger = get_logger(__name__)


class WindowActions:
    @staticmethod
    def driver() -> WebDriver:
        return Browser().get_driver()

    @staticmethod
    def current_handle() -> str:
        handle = WindowActions.driver().current_window_handle
        logger.info("Current window handle received: handle='%s'", handle)
        return handle

    @staticmethod
    def handles() -> list[str]:
        handles = WindowActions.driver().window_handles
        logger.info("Window handles received: count=%s, handles=%s", len(handles), handles)
        return handles

    @staticmethod
    def switch_to(handle: str) -> None:
        logger.info("Switching to window: handle='%s'", handle)
        WindowActions.driver().switch_to.window(handle)
        logger.info("Switched to window: handle='%s', url='%s'", handle, WindowActions.driver().current_url)

    @staticmethod
    def switch_to_new_window(old_handles: list[str], timeout: int | None = None) -> str:
        old_handles_set = set(old_handles)
        logger.info("Waiting for new window: old_handles=%s, timeout=%s", old_handles, timeout)

        def _new_window_is_opened(driver: WebDriver) -> str | bool:
            for handle in driver.window_handles:
                if handle not in old_handles_set:
                    driver.switch_to.window(handle)
                    return handle
            return False

        handle = Waiter.until(_new_window_is_opened, timeout)
        logger.info("New window opened: handle='%s', handles=%s", handle, WindowActions.driver().window_handles)
        return handle

    @staticmethod
    def close_current_and_switch_to(handle: str) -> None:
        logger.info("Closing current window and switching back: target_handle='%s'", handle)
        WindowActions.driver().close()
        WindowActions.switch_to(handle)
