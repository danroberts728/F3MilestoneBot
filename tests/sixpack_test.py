import unittest
import unittest.mock as mock
from datetime import datetime
from freezegun import freeze_time

import MilestoneTrigger.sixpack_milestsones as milestones

today = '2022-12-04'

class TestSixPack(unittest.TestCase):
    def test_emptyquery(self):
        with mock.patch('mysql.connector.connection') as mock_conn:
            mock_conn.cursor = mock.MagicMock()
            mock_conn.cursor.fetchall = []

            result = milestones.get(mock_conn, 'US/Central')

            assert len(result) == 0

    @freeze_time('2022-12-04 14:00:00')
    def test_oneresult(self):
        with mock.patch('mysql.connector.connection') as mock_conn:
            cursor = mock.MagicMock()
            mock_conn.cursor.return_value = cursor
            cursor.fetchall.return_value = [
                ('Cheerio', 'U254', '2022-11-28', '2022-12-03', 6)
            ]

            result = milestones.get(mock_conn, 'US/Central')

            assert len(result) == 1
            assert "<@U254>" in result[0] 
            assert "," not in result[0]
            assert "and " not in result[0]

    @freeze_time('2022-12-04 14:00:00')
    def test_tworesults(self):
        with mock.patch('mysql.connector.connection') as mock_conn:
            cursor = mock.MagicMock()
            mock_conn.cursor.return_value = cursor
            cursor.fetchall.return_value = [
                ('Cheerio', 'U254', '2022-11-28', '2022-12-03', 6),
                ('Crafty', 'U253', '2022-11-28', '2022-12-03', 6)
            ]

            result = milestones.get(mock_conn, 'US/Central')

            assert len(result) == 1
            assert "<@U254>" in result[0] 
            assert "," not in result[0]
            assert "and " in result[0]

    @freeze_time('2022-12-04 14:00:00')
    def test_manyresults(self):
        with mock.patch('mysql.connector.connection') as mock_conn:
            cursor = mock.MagicMock()
            mock_conn.cursor.return_value = cursor
            cursor.fetchall.return_value = [
                ('Cheerio', 'U254', '2022-11-28', '2022-12-03', 6),
                ('Crafty', 'U253', '2022-11-28', '2022-12-03', 6),
                ('Cheerio', 'U254', '2022-11-28', '2022-12-03', 6),
            ]

            result = milestones.get(mock_conn, 'US/Central')

            assert len(result) == 1
            assert "<@U254>" in result[0] 
            assert "," in result[0]
            assert "and " in result[0]

        
if __name__ == 'main':
    unittest.main()