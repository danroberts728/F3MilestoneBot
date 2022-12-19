import unittest
import unittest.mock as mock
from datetime import datetime
from freezegun import freeze_time

import MilestoneTrigger.max_attendance_milestone as milestones

class TestAttendance(unittest.TestCase):
    @freeze_time('2022-12-19 14:00:00')
    def test_nottoday(self):
        with mock.patch('mysql.connector.connection') as mock_conn:
            mock_conn.cursor = mock.MagicMock()
            mock_conn.cursor.fetchall = [
                ('2022-01-28', 'ao-slagheap', 'Hammy', '43', 'U02B5JT7R53')
            ]

            result = milestones.get(mock_conn, 'US/Central')

            assert len(result) == 0

    @freeze_time('2022-12-10 14:00:00')
    def test_match(self):
        with mock.patch('mysql.connector.connection') as mock_conn:
            cursor = mock.MagicMock()
            mock_conn.cursor.return_value = cursor
            cursor.fetchall.return_value = [
                ('2022-12-10', 'ao-houseofpaine', 'Breach', '47', 'U02B5JT7R43')
            ]

            result = milestones.get(mock_conn, 'US/Central')

            assert len(result) == 1

    @freeze_time('2022-12-19 14:00:00')
    def test_tie(self):
        with mock.patch('mysql.connector.connection') as mock_conn:
            mock_conn.cursor = mock.MagicMock()
            mock_conn.cursor.fetchall = [
                ('2022-01-28', 'ao-slagheap', 'Hammy', '43', 'U02B5JT7R53'),
                ('2022-12-19', 'ao-houseofpaine', 'Breach', '43', 'U02B5JT7R43')
            ]

            result = milestones.get(mock_conn, 'US/Central')

            assert len(result) == 0