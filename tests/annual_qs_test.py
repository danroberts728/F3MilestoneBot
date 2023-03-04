import unittest
import unittest.mock as mock
import datetime, pytz
from freezegun import freeze_time

import MilestoneTrigger.annual_qs_milestone as milestones

template ="Testing pax ${pax} qs_num ${qs_num} qs_ord ${qs_ord} last_q ${last_q} rank_num ${rank_num} rank_ord ${rank_ord} pax_tag ${pax_tag} current_year ${current_year}"

class TestAnnualQs(unittest.TestCase):
    @freeze_time('2022-12-04 14:00:00')
    def test_emptyquery(self):
        with mock.patch('mysql.connector.connection') as mock_conn:
            mock_conn.cursor = mock.MagicMock()
            mock_conn.cursor.fetchall = []

            result = milestones.get(mock_conn, 5, 'US/Central', template)

            assert len(result) == 0

    @freeze_time('2022-12-04 14:00:00')
    def test_oneresult(self):
        with mock.patch('mysql.connector.connection') as mock_conn:
            cursor = mock.MagicMock()
            mock_conn.cursor.return_value = cursor
            cursor.fetchall.return_value = [
                ('Spit Valve', 6, '2022-12-04', 1, 'U257', '2022')
            ]

            result = milestones.get(mock_conn, 6, 'US/Central', template)

            assert len(result) == 1
            assert "pax Spit Valve" in result[0]
            assert "qs_num 6" in result[0]
            assert "qs_ord 6th" in result[0]
            assert "last_q 2022-12-04" in result[0] 
            assert "rank_num 1" in result[0]
            assert "rank_ord 1st" in result[0]
            assert "U257" in result[0]
            assert "current_year 2022" in result[0]

    @freeze_time('2022-12-04 14:00:00')
    def test_manyresults(self):
        with mock.patch('mysql.connector.connection') as mock_conn:
            cursor = mock.MagicMock()
            mock_conn.cursor.return_value = cursor
            cursor.fetchall.return_value = [
                ('Spit Valve', 20, '2022-12-04', 1, 'U257', '2022'),
                ('Ethanol', 6, '2022-12-04', 2, 'U258', '2022'),  # Match
                ('Crafty', 6, '2022-12-04', 3, 'U259', '2022'),  # Match
                ('Breach', 5, '2022-12-04', 4, 'U260', '2022'),
                ('Eskimo', 6, '2022-12-03', 5, 'U261', '2022')
            ]

            result = milestones.get(mock_conn, 6, "US/Central", template)

            assert len(result) == 2

            crafty = list(filter(lambda r: 'U259' in r, result))[0]
            ethanol =  list(filter(lambda r: 'U258' in r, result))[0]

            assert "pax Crafty" in crafty
            assert "qs_num 6" in crafty
            assert "qs_ord 6th" in crafty
            assert "last_q 2022-12-04" in crafty
            assert "rank_num 3" in crafty
            assert "rank_ord 3rd" in crafty
            assert "current_year 2022" in crafty

            assert "pax Ethanol" in ethanol 
            assert "qs_num 6" in ethanol
            assert "qs_ord 6th" in ethanol
            assert "last_q 2022-12-04" in ethanol
            assert "rank_num 2" in ethanol
            assert "rank_ord 2nd" in ethanol
            assert "current_year 2022" in ethanol

if __name__ == 'main':
    unittest.main()