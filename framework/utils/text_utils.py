import re


class TextUtils:
    @staticmethod
    def normalize(value: str) -> str:
        return " ".join(value.split())

    @staticmethod
    def normalize_price(value: str) -> str:
        text = TextUtils.normalize(value)
        if "free" in text.lower():
            return "Free"
        return text.rstrip(".").strip()

    @staticmethod
    def extract_first_number(value: str) -> int:
        match = re.search(r"\d[\d\s,.\u00A0]*", value)
        if match is None:
            raise ValueError(f"Could not extract number from text: {value!r}")
        return int(re.sub(r"\D", "", match.group(0)))
