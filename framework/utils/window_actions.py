from selenium.webdriver.remote.webdriver import WebDriver

from framework.core.browser import Browser
from framework.utils.waiter import Waiter


class WindowActions:
    @staticmethod
    def driver() -> WebDriver:
        return Browser().driver

    @staticmethod
    def current_handle() -> str:
        return WindowActions.driver().current_window_handle

    @staticmethod
    def handles() -> list[str]:
        return WindowActions.driver().window_handles

    @staticmethod
    def switch_to(handle: str) -> None:
        WindowActions.driver().switch_to.window(handle)

    @staticmethod
    def switch_to_new_window(old_handles: list[str], timeout: int | None = None) -> str:
        old_handles_set = set(old_handles)

        def _new_window_is_opened(driver: WebDriver) -> str | bool:
            for handle in driver.window_handles:
                if handle not in old_handles_set:
                    driver.switch_to.window(handle)
                    return handle
            return False

        return Waiter.until(_new_window_is_opened, timeout)

    @staticmethod
    def close_current_and_switch_to(handle: str) -> None:
        WindowActions.driver().close()
        WindowActions.switch_to(handle)
