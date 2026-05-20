from framework.elements.base_element import BaseElement


class TextElement(BaseElement):
    @property
    def element_type(self) -> str:
        return "text"
