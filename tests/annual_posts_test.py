import unittest
import unittest.mock as mock
import datetime, pytz
from freezegun import freeze_time

import MilestoneTrigger.annual_posts_milestones as milestones

template ="Testing pax ${pax} last_post ${last_post} posts_num ${posts_num} pax_tag ${pax_tag} posts_ord ${posts_ord} posts_weekly_avg ${posts_weekly_avg} current_year ${current_year}"

class TestAnnualPosts(unittest.TestCase):
    @freeze_time('2022-12-04 14:00:00')
    def test_emptyquery(self):
        with mock.patch('mysql.connector.connection') as mock_conn:
            mock_conn.cursor = mock.MagicMock()
            mock_conn.cursor.fetchall = []

            result = milestones.get(mock_conn, 50, 'US/Central', template, False)

            assert len(result) == 0

    @freeze_time('2022-12-04 14:00:00')
    def test_oneresult(self):
        with mock.patch('mysql.connector.connection') as mock_conn:
            cursor = mock.MagicMock()
            mock_conn.cursor.return_value = cursor
            cursor.fetchall.return_value = [
                ('Spit Valve', 200, 4.48, '2022-12-04', '2022', 'U257')
            ]

            result = milestones.get(mock_conn, 200, 'US/Central', template, False)

            assert len(result) == 1
            assert "pax Spit Valve" in result[0]
            assert "last_post 2022-12-04" in result[0]
            assert "posts_num 200" in result[0]
            assert "pax_tag <@U257>" in result[0] 
            assert "posts_ord 200th" in result[0]
            assert "posts_weekly_avg 4.48" in result[0]
            assert "current_year 2022" in result[0]

    @freeze_time('2022-12-04 14:00:00')
    def test_manyresults(self):
        with mock.patch('mysql.connector.connection') as mock_conn:
            cursor = mock.MagicMock()
            mock_conn.cursor.return_value = cursor
            cursor.fetchall.return_value = [
                ('Spit Valve', 250, 4.1, '2022-12-04', '2022', 'U1'),
                ('Crafty', 200, 4.2, '2022-12-04', '2022', 'U2'), # Match
                ('Ethanol', 200, 4.3, '2022-12-04', '2022', 'U3'), # Match
                ('Breach', 200, 4.4, '2022-12-03', '2022', 'U4'),
                ('Gipper', 187, 4.5, '2022-12-04', '2022', 'U5')
            ]

            result = milestones.get(mock_conn, 200, "US/Central", template, False)

            assert len(result) == 2

            crafty = list(filter(lambda r: 'U2' in r, result))[0]
            ethanol =  list(filter(lambda r: 'U3' in r, result))[0]

            assert "pax Crafty" in crafty 
            assert "last_post 2022-12-04" in crafty
            assert "posts_num 200" in crafty
            assert "pax_tag <@U2>" in crafty
            assert "posts_ord 200th" in crafty
            assert "posts_weekly_avg 4.2" in crafty
            assert "current_year 2022" in crafty

            assert "pax Ethanol" in ethanol 
            assert "last_post 2022-12-04" in ethanol
            assert "posts_num 200" in ethanol
            assert "pax_tag <@U3>" in ethanol
            assert "posts_ord 200th" in ethanol
            assert "posts_weekly_avg 4.3" in ethanol
            assert "current_year 2022" in ethanol

    @freeze_time('2022-12-04 14:00:00')
    def test_disable_first_year(self):
        with mock.patch('mysql.connector.connection') as mock_conn:
            cursor = mock.MagicMock()
            mock_conn.cursor.return_value = cursor
            cursor.fetchall.return_value = [
                ('Spit Valve', 250, 4.1, '2022-12-04', '2022', 'U1'),
                ('Crafty', 200, 4.2, '2022-12-04', '2022', 'U2'),
                ('Ethanol', 200, 4.3, '2022-12-04', '2021', 'U3'), # Match
                ('Breach', 200, 4.4, '2022-12-03', '2022', 'U4'),
                ('Gipper', 187, 4.5, '2022-12-04', '2022', 'U5')
            ]

            result = milestones.get(mock_conn, 200, "US/Central", template, True)

            assert len(result) == 1

            ethanol =  list(filter(lambda r: 'U3' in r, result))[0]

            assert "pax Ethanol" in ethanol 
            assert "last_post 2022-12-04" in ethanol
            assert "posts_num 200" in ethanol
            assert "pax_tag <@U3>" in ethanol
            assert "posts_ord 200th" in ethanol
            assert "posts_weekly_avg 4.3" in ethanol
            assert "current_year 2022" in ethanol

if __name__ == 'main':
    unittest.main()