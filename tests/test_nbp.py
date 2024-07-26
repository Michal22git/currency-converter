import unittest
from datetime import datetime
from unittest.mock import patch, Mock

from requests.models import Response

from task.connectors.nbp.data_fetcher import NBP


class TestNBP(unittest.TestCase):
    @patch('requests.get')
    def test_get_rate_success(self, mock_get):
        mock_response = Mock(spec=Response)
        mock_response.status_code = 200
        today_date = datetime.today().strftime('%Y-%m-%d')
        mock_response.json.return_value = {
            'rates': [
                {'mid': 4.20, 'effectiveDate': today_date}
            ]
        }
        mock_get.return_value = mock_response
        nbp = NBP()
        rate = nbp.get_rate('USD')
        self.assertEqual(rate, (4.20, today_date))
