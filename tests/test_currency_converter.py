import unittest
from unittest.mock import Mock

from task.connectors.local.file_reader import FileReader
from task.connectors.nbp.data_fetcher import NBP
from task.currency_converter import PriceCurrencyConverterToPLN, ConvertedPricePLN


class TestPriceCurrencyConverter(unittest.TestCase):
    def test_convert_to_pln_with_valid_rate(self):
        mock_file_reader = Mock(spec=FileReader)
        mock_file_reader.get_rate.return_value = (4.2, '2024-06-25')
        converter = PriceCurrencyConverterToPLN(mock_file_reader)
        converted = converter.convert_to_pln(currency='USD', price=100.0)
        expected_result = ConvertedPricePLN(
            price_in_source_currency=100.0,
            currency='USD',
            currency_rate=4.2,
            currency_rate_fetch_date='2024-06-25',
            price_in_pln=420.0
        )
        self.assertEqual(converted, expected_result)

    def test_convert_to_pln_with_invalid_rate(self):
        mock_nbp = Mock(spec=NBP)
        mock_nbp.get_rate.return_value = None
        converter = PriceCurrencyConverterToPLN(mock_nbp)
        converted = converter.convert_to_pln(currency='EUR', price=50.0)
        self.assertIsNone(converted)
        mock_nbp.get_rate.assert_called_once_with('EUR')
