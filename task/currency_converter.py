from dataclasses import dataclass
from typing import Union

from task.logger import logger
from task.connectors.base_classes import RateProvider


@dataclass(frozen=True)
class ConvertedPricePLN:
    price_in_source_currency: float
    currency: str
    currency_rate: float
    currency_rate_fetch_date: str
    price_in_pln: float


class PriceCurrencyConverterToPLN:
    def __init__(self, rate_provider: Union[RateProvider]) -> None:
        self.rate_provider = rate_provider

    def convert_to_pln(self, *, currency: str, price: float) -> ConvertedPricePLN | None:
        try:
            rate_output = self.rate_provider.get_rate(currency)
            if rate_output:
                rate, rate_date = rate_output
                price_in_pln = round(price * rate, 2)
                return ConvertedPricePLN(
                    price_in_source_currency=price,
                    currency=currency,
                    currency_rate=rate,
                    currency_rate_fetch_date=rate_date,
                    price_in_pln=price_in_pln
                )
            else:
                logger.error("Couldn't fetch rate info")
                return None
        except Exception as e:
            logger.error(f"Failed to fetch rate info: {e}")
            return None
