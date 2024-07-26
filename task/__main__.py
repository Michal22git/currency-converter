import argparse
import traceback

from task.connectors.database.json import JsonFileDatabaseConnector
from task.connectors.database.prod_sql import SqliteDatabaseConnector
from task.connectors.local.file_reader import FileReader
from task.connectors.nbp.data_fetcher import NBP
from task.currency_converter import PriceCurrencyConverterToPLN
from task.logger import logger

try:
    parser = argparse.ArgumentParser(description='Currency converter. Converts any amount of given currency into PLN using selected source.')
    parser.add_argument('mode', type=str, choices=['dev', 'prod'], help='Script run mode')
    parser.add_argument('amount', type=float, help='Amount to convert')
    parser.add_argument('currency', type=str, help='Base currency code')
    parser.add_argument('source', type=str, choices=['local', 'nbp'], help='Source of currency rates')

    args = parser.parse_args()

    if args.mode == 'dev':
        database_connector = JsonFileDatabaseConnector()
    elif args.mode == 'prod':
        database_connector = SqliteDatabaseConnector()

    if args.source == 'local':
        rate_provider = FileReader()
    elif args.source == 'nbp':
        rate_provider = NBP()

    converter = PriceCurrencyConverterToPLN(rate_provider)
    result = converter.convert_to_pln(currency=args.currency, price=args.amount)

    if result:
        database_connector.save({
            "currency": result.currency,
            "rate": result.currency_rate,
            "price_in_pln": result.price_in_pln,
            "date": result.currency_rate_fetch_date
        })
        logger.info(f"Converted {args.amount} {args.currency} to {result.price_in_pln} PLN")
    else:
        logger.error("Failed to convert")
except Exception as err:
    logger.error(traceback.format_exc())
