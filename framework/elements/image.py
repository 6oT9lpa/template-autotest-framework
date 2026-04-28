from framework.elements.base_element import BaseElement


class Image(BaseElement):
    def source(self) -> str | None:
        return self.get_attribute("src")

    def alt_text(self) -> str | None:
        return self.get_attribute("alt")
