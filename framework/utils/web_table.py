from collections.abc import Callable
from typing import TypeVar

from selenium.webdriver.remote.webelement import WebElement

from framework.core.browser import Browser
from framework.utils.text import TextUtils
from framework.utils.waiter import Locator

Record = TypeVar("Record")


class WebTableUtils:
    @staticmethod
    def records(
        row_locator: Locator,
        cell_locator: Locator,
        mapper: Callable[[list[str]], Record | None],
    ) -> list[Record]:
        records: list[Record] = []
        for row in WebTableUtils._visible_rows(row_locator):
            record = mapper(WebTableUtils._cell_texts(row, cell_locator))
            if record is not None:
                records.append(record)
        return records

    @staticmethod
    def click_row_button(
        row_locator: Locator,
        cell_locator: Locator,
        button_locator: Locator,
        expected_record: Record,
        mapper: Callable[[list[str]], Record | None],
    ) -> bool:
        row = WebTableUtils._find_row(row_locator, cell_locator, expected_record, mapper)
        if row is None:
            return False

        row.find_element(*button_locator).click()
        return True

    @staticmethod
    def _find_row(
        row_locator: Locator,
        cell_locator: Locator,
        expected_record: Record,
        mapper: Callable[[list[str]], Record | None],
    ) -> WebElement | None:
        for row in WebTableUtils._visible_rows(row_locator):
            if mapper(WebTableUtils._cell_texts(row, cell_locator)) == expected_record:
                return row
        return None

    @staticmethod
    def _visible_rows(row_locator: Locator) -> list[WebElement]:
        return [
            row
            for row in Browser().get_driver().find_elements(*row_locator)
            if row.is_displayed()
        ]

    @staticmethod
    def _cell_texts(row: WebElement, cell_locator: Locator) -> list[str]:
        return [
            TextUtils.normalize(cell.text)
            for cell in row.find_elements(*cell_locator)
        ]
