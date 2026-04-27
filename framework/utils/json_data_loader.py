import json
from pathlib import Path

from framework.core.singleton import SingletonMeta


class JsonDataLoader(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self._data_root = Path(__file__).resolve().parents[2] / "data"
        self._cache: dict[str, dict] = {}

    def load(self, file_name: str) -> dict:
        if file_name not in self._cache:
            file_path = self._data_root / file_name

            with file_path.open(encoding="utf-8") as data_file:
                self._cache[file_name] = json.load(data_file)

        return self._cache[file_name]
