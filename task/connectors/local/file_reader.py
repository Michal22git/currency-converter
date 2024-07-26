import json
from typing import Any

from task.config import LOCAL_RATES
from task.connectors.base_classes import RateProvider


class FileReader(RateProvider):
    def __init__(self):
        self._data = self._read_data()

    @staticmethod
    def _read_data() -> dict[str, Any]:
        with open(LOCAL_RATES, 'r') as file:
            return json.load(file)

    def get_rate(self, currency: str) -> tuple[float, str] | None:
        currency = currency.upper()
        if currency in self._data:
            sorted_data = sorted(self._data[currency], key=lambda x: x['date'], reverse=True)
            if sorted_data:
                rate_info = sorted_data[0]
                return rate_info['rate'], rate_info['date']
        return None
