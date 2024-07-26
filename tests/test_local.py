import unittest
from unittest.mock import patch, mock_open

from task.connectors.local.file_reader import FileReader


class TestFileReader(unittest.TestCase):
    @patch('task.connectors.local.file_reader.LOCAL_RATES', 'mock_file.json')
    @patch('task.connectors.local.file_reader.open', new_callable=mock_open, read_data='{"USD": [{"rate": 3.75, "date": "2024-06-26"}, {"rate": 3.70, "date": "2024-06-25"}], "EUR": [{"rate": 4.30, "date": "2024-06-26"}]}')
    def setUp(self, mock_file):
        self.file_reader = FileReader()

    def test_get_rate_existing_currency(self):
        rate, date = self.file_reader.get_rate('USD')
        self.assertEqual(rate, 3.75)
        self.assertEqual(date, "2024-06-26")

    def test_get_rate_nonexistent_currency(self):
        result = self.file_reader.get_rate('HEH')
        self.assertIsNone(result)

    def test_get_rate_case_insensitive(self):
        rate, date = self.file_reader.get_rate('usd')
        self.assertEqual(rate, 3.75)
        self.assertEqual(date, "2024-06-26")

    def test_get_rate_returns_most_recent(self):
        rate, date = self.file_reader.get_rate('USD')
        self.assertEqual(rate, 3.75)
        self.assertEqual(date, "2024-06-26")
