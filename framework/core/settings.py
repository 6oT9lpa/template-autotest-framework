from typing import Any

from framework.utils.json_data_loader import JsonDataLoader
from framework.core.singleton import SingletonMeta
from framework.models.config import Config


class ConfigManager(metaclass=SingletonMeta):
    CONFIG_FILE_NAME = "config.json"

    def __init__(self) -> None:
        self.config = Config.from_dict(JsonDataLoader().load(self.CONFIG_FILE_NAME))


class TestDataManager(metaclass=SingletonMeta):
    __test__ = False
    TEST_DATA_FILE_NAME = "test_data.json"

    def __init__(self) -> None:
        self.data = JsonDataLoader().load(self.TEST_DATA_FILE_NAME)

    def get(self, key: str, default: Any = None) -> Any:
        return self.data.get(key, default)
