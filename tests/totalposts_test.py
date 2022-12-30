import unittest
import unittest.mock as mock
import datetime, pytz

import MilestoneTrigger.total_posts_milestones as milestones

template ="Testing Name ${pax} last_post ${last_post} rank_num ${rank_num} pax_id ${pax_id} pax_tag ${pax_tag} posts_ord ${posts_ord} rank_ord ${rank_ord}"

today = datetime.datetime.utcnow().replace(
            tzinfo=datetime.timezone.utc).astimezone(
                tz=pytz.timezone("US/Central")).strftime('%Y-%m-%d')

class TestTotalPosts(unittest.TestCase):
    def test_emptyquery(self):
        with mock.patch('mysql.connector.connection') as mock_conn:
            mock_conn.cursor = mock.MagicMock()
            mock_conn.cursor.fetchall = []

            result = milestones.get(mock_conn, 50, 'US/Central', template)

            assert len(result) == 0

    def test_oneresult(self):
        with mock.patch('mysql.connector.connection') as mock_conn:
            cursor = mock.MagicMock()
            mock_conn.cursor.return_value = cursor
            cursor.fetchall.return_value = [
                ('Breach (Aaron Smith)', today, 50, 1, 'U257')
            ]

            result = milestones.get(mock_conn, 50, 'US/Central', template)

            assert len(result) == 1
            assert "<@U257>" in result[0] 
            assert "50th" in result[0]
            assert "1st" in result[0]

    def test_manyresults(self):
        with mock.patch('mysql.connector.connection') as mock_conn:
            cursor = mock.MagicMock()
            mock_conn.cursor.return_value = cursor
            cursor.fetchall.return_value = [
                ('Cheerio', today, 257, 1, 'U254'),
                ('Ethanol', '2001-01-01', 59, 2, 'U255'),
                ('Spit Valve', '2005-05-22', 50, 3, 'U345'),
                ('Crafty', today, 50, 4, 'U256'),
                ('Breach (Aaron Smith)', today, 50, 5, 'U257')
            ]

            result = milestones.get(mock_conn, 50, 'US/Central', template)

            assert len(result) == 2

            breach =  list(filter(lambda r: 'U257' in r, result))[0]
            crafty = list(filter(lambda r: 'U256' in r, result))[0]
            assert "<@U256>" in crafty 
            assert "50th" in crafty
            assert "4th" in crafty
            assert "<@U257>" in breach
            assert "50th" in breach
            assert "5th" in breach

        
if __name__ == 'main':
    unittest.main()