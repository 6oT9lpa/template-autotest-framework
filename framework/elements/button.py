from framework.elements.base_element import BaseElement


class Button(BaseElement):
    @property
    def element_type(self) -> str:
        return "button"
