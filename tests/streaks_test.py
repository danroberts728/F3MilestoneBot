import unittest
import unittest.mock as mock
import datetime, pytz

import MilestoneTrigger.streak_milestones as milestones

today = datetime.datetime.utcnow().replace(
            tzinfo=datetime.timezone.utc).astimezone(
                tz=pytz.timezone("US/Central")).strftime('%Y-%m-%d')

template = "Testing Name ${pax} streak_count ${streak_count} streak_count_ord ${streak_count_ord} last_post ${last_post} pax_tag ${pax_tag}"

class TestStreaks(unittest.TestCase):
    def test_emptyquery(self):
        with mock.patch('mysql.connector.connection') as mock_conn:
            mock_conn.cursor = mock.MagicMock()
            mock_conn.cursor.fetchall = []

            result = milestones.get(mock_conn, 10, 'US/Central', template)

            assert len(result) == 0

    def test_oneresult(self):
        with mock.patch('mysql.connector.connection') as mock_conn:
            cursor = mock.MagicMock()
            mock_conn.cursor.return_value = cursor
            cursor.fetchall.return_value = [
                ('Breach (Aaron Smith)', 258, 20, today, 'U257')
            ]

            result = milestones.get(mock_conn, 10, 'US/Central', template)

            assert len(result) == 1
            assert "<@U257>" in result[0] 
            assert "20" in result[0]
            assert today in result[0]
            assert "20th" in result[0]

    def test_manyresults(self):
        with mock.patch('mysql.connector.connection') as mock_conn:
            cursor = mock.MagicMock()
            mock_conn.cursor.return_value = cursor
            cursor.fetchall.return_value = [
                ('Cheerio', 257, 19, today, 'U254'),    # No
                ('Ethanol', 3, 20, today, 'U255'),      # Yes
                ('Spit Valve',60, 10, '2005-05-22', 'U345'),   # No
                ('Crafty', 8, 50, today, 'U256'),       # Yes
                ('Breach (Aaron Smith)', 50, 12, today, 'U257') #No
            ]

            result = milestones.get(mock_conn, 10, 'US/Central', template)

            assert len(result) == 2

            ethanol =  list(filter(lambda r: 'U255' in r, result))[0]
            crafty = list(filter(lambda r: 'U256' in r, result))[0]
            assert "<@U256>" in crafty 
            assert "50" in crafty
            assert "50th" in crafty
            assert "<@U255>" in ethanol
            assert "20th" in ethanol
            assert "20" in ethanol

        
if __name__ == 'main':
    unittest.main()