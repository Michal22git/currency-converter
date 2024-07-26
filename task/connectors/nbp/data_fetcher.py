import requests

from task.logger import logger
from task.config import NBP_API_ENDPOINT_URL
from task.connectors.base_classes import RateProvider


class NBP(RateProvider):
    def get_rate(self, currency: str) -> tuple[float, str] | None:
        try:
            req = requests.get(
                NBP_API_ENDPOINT_URL + currency,
                headers={
                    "Accept": "application/json"
                }
            )

            if req.ok:
                rate_info = req.json()['rates'][0]
                return rate_info['mid'], rate_info['effectiveDate']
            else:
                logger.error(f"Failed to request nbp: {req.status_code}")
                return None
        except Exception as e:
            logger.error(f"Error while fetching data from nbp: {e}")
            return None
