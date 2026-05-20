from framework.utils.json_data_loader import JsonDataLoader
from framework.core.singleton import SingletonMeta
from framework.models.browser_config import BrowserConfig
from framework.models.config import Config
from framework.models.test_data import TestData


class ConfigManager(metaclass=SingletonMeta):
    CONFIG_FILE_NAME = "config.json"
    BROWSER_CONFIG_FILE_NAME = "browser_config.json"

    def __init__(self) -> None:
        self.config = Config.model_validate(
            JsonDataLoader().load(self.CONFIG_FILE_NAME)
        )
        self.browser_config = BrowserConfig.model_validate(
            JsonDataLoader().load(self.BROWSER_CONFIG_FILE_NAME)
        )


class TestDataManager(metaclass=SingletonMeta):
    __test__ = False

    TEST_DATA_FILE_NAME = "test_data.json"

    def __init__(self) -> None:
        self._data = TestData.model_validate(
            JsonDataLoader().load(self.TEST_DATA_FILE_NAME)
        )

    def __getattr__(self, item):
        return getattr(self._data, item)
