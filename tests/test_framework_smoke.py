from framework.core.browser_factories import BrowserFactory
from framework.core.settings import ConfigManager, TestDataManager as TestData
from framework.elements import Button, ElementFactory, Input, TextElement
from framework.models.config import LoggingConfig


def test_framework_smoke_imports_and_config(step) -> None:
    config = ConfigManager().config

    assert config.base_url
    assert config.explicit_wait >= 0
    assert isinstance(TestData().data, dict)
    assert LoggingConfig.from_dict({"console_enabled": False}).console_enabled is False
    assert sorted(BrowserFactory._factories) == ["chrome", "edge", "firefox"]
    assert Button.__name__ == "Button"
    assert ElementFactory.__name__ == "ElementFactory"
    assert Input.__name__ == "Input"
    assert TextElement.__name__ == "TextElement"
