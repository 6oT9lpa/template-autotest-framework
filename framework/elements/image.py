from framework.elements.base_element import BaseElement
from framework.constants import HtmlAttribute


class Image(BaseElement):
    @property
    def element_type(self) -> str:
        return "image"

    def source(self) -> str | None:
        return self.get_attribute(HtmlAttribute.SRC)

    def alt_text(self) -> str | None:
        return self.get_attribute(HtmlAttribute.ALT)
