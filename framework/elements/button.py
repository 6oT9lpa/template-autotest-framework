from framework.elements.base_element import BaseElement


class Button(BaseElement):
    def click(self) -> None:
        super().click()

    def is_enabled(self) -> bool:
        return self.find_element().is_enabled()
