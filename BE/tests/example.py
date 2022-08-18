from datetime import datetime
from unittest.mock import patch, Mock

import unittest

from app.main import get_day_of_week


class GetDayOfWeek(unittest.TestCase):

    def test_get_day_of_week(self):
        dow = datetime.now().strftime("%A")
        self.assertEqual(dow, get_day_of_week()['day'])

    @patch('app.main.get_datetime_now')
    def test_mocked_get_day_of_week(self, mock_get_dow: Mock):
        # Assign new value to force now() return same result
        mock_get_dow.return_value = datetime(2022, 8, 7)
        expected = 'Sunday'
        self.assertEqual(expected, get_day_of_week()['day'])
