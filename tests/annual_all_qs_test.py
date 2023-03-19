import unittest
import unittest.mock as mock
import datetime, pytz
from freezegun import freeze_time

import MilestoneTrigger.annual_all_qs_milestone as milestones

template ="Testing Name ${pax} pax_tag ${pax_tag} ao ${ao} last_q ${last_q} unique_q_count ${unique_q_count} unique_q_count_ord ${unique_q_count_ord} current_year ${current_year}"

class TestAnnualAllQs(unittest.TestCase):
    def test_emptyquery(self):
        with mock.patch('mysql.connector.connection') as mock_conn:
            mock_conn.cursor = mock.MagicMock()
            mock_conn.cursor.fetchall = []

            result = milestones.get(mock_conn, 'US/Central', template)

            assert len(result) == 0

    @freeze_time('2022-12-04 14:00:00')
    def test_oneresult(self):
        with mock.patch('mysql.connector.connection') as mock_conn:
            cursor = mock.MagicMock()
            mock_conn.cursor.return_value = cursor
            cursor.fetchall.return_value = [
                ('Breach', 'ao-golem', 1, '2022-12-04', 3, 'U257', '2022'),
                ('Breach', 'ao-slagheap', 1, '2022-12-02', 3, 'U257', '2022'),
                ('Breach', 'ao-houseofpaine', 1, '2022-12-01', 3, 'U257', '2022'),
                ('Doogie', 'ao-slagheap', 1, '2022-12-03', 3, 'U258', '2022'),
                ('Doogie', 'ao-houseofpaine', 1, '2022-12-02', 3, 'U258', '2022'),
                ('Doogie', 'ao-golem', 1, '2022-12-01', 3, 'U258', '2022')
            ]

            result = milestones.get(mock_conn, 'US/Central', template)

            assert len(result) == 1
            assert 'Name Breach' in result[0]
            assert "<@U257>" in result[0] 
            assert "ao ao-golem" in result[0]
            assert "last_q 2022-12-04" in result[0]
            assert "unique_q_count 3" in result[0]
            assert "unique_q_count_ord 3rd" in result[0]
            assert "current_year 2022" in result[0]

    @freeze_time('2022-12-04 14:00:00')
    def test_manyresults(self):
        with mock.patch('mysql.connector.connection') as mock_conn:
            cursor = mock.MagicMock()
            mock_conn.cursor.return_value = cursor
            cursor.fetchall.return_value = [
                ('Breach', 'ao-golem', 1, '2022-12-04', 3, 'U257', '2022'),
                ('Breach', 'ao-slagheap', 1, '2022-12-02', 3, 'U257', '2022'),
                ('Breach', 'ao-houseofpaine', 1, '2022-12-01', 3, 'U257', '2022'),
                ('Doogie', 'ao-slagheap', 1, '2022-12-04', 3, 'U258', '2022'),
                ('Doogie', 'ao-houseofpaine', 1, '2022-12-01', 3, 'U258', '2022'),
                ('Doogie', 'ao-golem', 1, '2022-11-01', 3, 'U258', '2022'),
                ('Crafty', 'ao-slagheap', 1, '2022-12-01', 3, 'U259', '2022'),
                ('Crafty', 'ao-houseofpaine', 1, '2022-10-02', 3, 'U259', '2022'),
                ('Crafty', 'ao-golem', 1, '2022-10-01', 3, 'U259', '2022')
            ]

            result = milestones.get(mock_conn, 'US/Central', template)

            assert len(result) == 2

            breach =  list(filter(lambda r: 'U257' in r, result))[0]
            doogie = list(filter(lambda r: 'U258' in r, result))[0]

            assert 'Name Breach' in breach
            assert "<@U257>" in breach
            assert "ao ao-golem" in breach
            assert "last_q 2022-12-04" in breach
            assert "unique_q_count 3" in breach
            assert "unique_q_count_ord 3rd" in breach
            assert "current_year 2022" in breach

            assert 'Name Doogie' in doogie
            assert "<@U258>" in doogie
            assert "ao ao-slagheap" in doogie
            assert "last_q 2022-12-04" in doogie
            assert "unique_q_count 3" in doogie
            assert "unique_q_count_ord 3rd" in doogie
            assert "current_year 2022" in doogie

        
if __name__ == 'main':
    unittest.main()