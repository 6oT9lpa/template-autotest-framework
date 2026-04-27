__all__ = [
    "JsonDataLoader",
    "JsActions",
    "Locator",
    "TextUtils",
    "Waiter",
    "xpath_literal",
]


def __getattr__(name: str):
    if name == "JsonDataLoader":
        from framework.utils.json_data_loader import JsonDataLoader

        return JsonDataLoader

    if name == "JsActions":
        from framework.utils.js_actions import JsActions

        return JsActions

    if name == "Locator":
        from framework.utils.waiter import Locator

        return Locator

    if name == "TextUtils":
        from framework.utils.text_utils import TextUtils

        return TextUtils

    if name == "Waiter":
        from framework.utils.waiter import Waiter

        return Waiter

    if name == "xpath_literal":
        from framework.utils.locator_utils import xpath_literal

        return xpath_literal

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
