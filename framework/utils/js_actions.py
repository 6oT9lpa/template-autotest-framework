from selenium.webdriver.remote.webelement import WebElement

from framework.core.browser import Browser


class JsActions:
    @staticmethod
    def click(element: WebElement) -> None:
        Browser().get_driver().execute_script("arguments[0].click();", element)

    @staticmethod
    def scroll_into_view(element: WebElement) -> None:
        Browser().get_driver().execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            element,
        )
