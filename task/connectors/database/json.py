import json
from typing import Any

from task.config import JSON_DB
from task.connectors.base_classes import DatabaseConnector


class JsonFileDatabaseConnector(DatabaseConnector):
    def __init__(self) -> None:
        self._data = self._read_data()

    @staticmethod
    def _read_data() -> dict:
        with open(JSON_DB, "r") as file:
            return json.load(file)

    def save(self, entity: dict[str, Any]) -> int:
        if self._data:
            key_id = int(max(self._data.keys(), key=int)) + 1
        else:
            key_id = 1

        new_input = {'id': key_id}
        entity = {k: v for k, v in entity.items() if k != 'id'}

        new_input.update(entity)

        self._data[str(key_id)] = new_input

        with open(JSON_DB, 'w') as file:
            json.dump(self._data, file, indent=2)
        return key_id

    def get_all(self) -> list[dict[str, Any]]:
        return list(self._data.values())

    def get_by_id(self, id: int) -> dict[str, Any] | None:
        return self._data.get(str(id), None)
