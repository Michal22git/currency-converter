import unittest
from unittest.mock import patch, mock_open

from task.connectors.database.json import JsonFileDatabaseConnector
from task.connectors.database.prod_sql import SqliteDatabaseConnector


class TestJsonFileDatabaseConnector(unittest.TestCase):
    def setUp(self):
        self.sample_entity = {
            "currency": "EUR",
            "rate": 0.9,
            "price_in_pln": 4.5,
            "date": "2024-06-26"
        }

    @patch("task.connectors.database.json.open", new_callable=mock_open)
    def test_save_and_get_by_id(self, mock_file):
        mock_file.return_value.read.return_value = '{}'
        connector = JsonFileDatabaseConnector()
        new_id = connector.save(self.sample_entity)
        self.assertEqual(new_id, 1)
        mock_file.return_value.read.return_value = '{"1": {"id": 1, "currency": "EUR", "rate": 0.9, "price_in_pln": 4.5, "date": "2024-06-26"}}'
        result = connector.get_by_id(1)
        self.assertIsNotNone(result)
        self.assertEqual(result["currency"], "EUR")
        self.assertEqual(result["rate"], 0.9)

    @patch("task.connectors.database.json.open", new_callable=mock_open)
    def test_get_all(self, mock_file):
        mock_file.return_value.read.return_value = '{"1": {"id": 1, "currency": "USD", "rate": 1.0, "price_in_pln": 4.0, "date": "2024-06-25"}}'
        connector = JsonFileDatabaseConnector()
        result = connector.get_all()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["currency"], "USD")

    @patch("task.connectors.database.json.open", new_callable=mock_open)
    def test_get_nonexistent_id(self, mock_file):
        mock_file.return_value.read.return_value = '{"1": {"id": 1, "currency": "USD", "rate": 1.0, "price_in_pln": 4.0, "date": "2024-06-25"}}'
        connector = JsonFileDatabaseConnector()
        result = connector.get_by_id(2)
        self.assertIsNone(result)


class TestSqliteDatabaseConnector(unittest.TestCase):
    def setUp(self):
        self.connector = SqliteDatabaseConnector('sqlite:///:memory:')
        self.sample_entity = {
            'currency': 'USD',
            'rate': 1.0,
            'price_in_pln': 4.0,
            'date': '2024-06-26'
        }

    def test_save_and_get_by_id(self):
        new_id = self.connector.save(self.sample_entity)
        self.assertIsInstance(new_id, int)
        retrieved_entity = self.connector.get_by_id(new_id)
        self.assertIsNotNone(retrieved_entity)
        self.assertEqual(retrieved_entity['currency'], 'USD')
        self.assertEqual(retrieved_entity['rate'], 1.0)
        self.assertEqual(retrieved_entity['price_in_pln'], 4.0)
        self.assertEqual(retrieved_entity['date'], '2024-06-26')

    def test_get_all(self):
        self.connector.save(self.sample_entity)
        self.connector.save({
            'currency': 'EUR',
            'rate': 0.9,
            'price_in_pln': 4.5,
            'date': '2024-06-27'
        })
        all_entities = self.connector.get_all()
        self.assertIsInstance(all_entities, list)
        self.assertGreaterEqual(len(all_entities), 2)

    def test_get_nonexistent_id(self):
        non_existent_entity = self.connector.get_by_id(9999)
        self.assertIsNone(non_existent_entity)
