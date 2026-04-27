from framework.elements.base_element import BaseElement
from framework.utils.text_utils import TextUtils


class TextElement(BaseElement):
    def normalized_text(self) -> str:
        return TextUtils.normalize(self.text())
