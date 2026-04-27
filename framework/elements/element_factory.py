from framework.elements.button import Button
from framework.elements.input import Input
from framework.elements.text_element import TextElement
from framework.utils.waiter import Locator

class ElementFactory:
    @staticmethod
    def button(locator: Locator, name: str) -> Button:
        return Button(locator, name)

    @staticmethod
    def input(locator: Locator, name: str) -> Input:
        return Input(locator, name)

    @staticmethod
    def text(locator: Locator, name: str) -> TextElement:
        return TextElement(locator, name)
