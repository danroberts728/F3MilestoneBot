import unittest
import unittest.mock as mock
import datetime, pytz
from freezegun import freeze_time

import MilestoneTrigger.all_aos_milestone as milestones

template ="Testing Name ${pax} last_post ${last_post} pax_tag ${pax_tag} ao_count ${ao_count} ao_count_ord ${ao_count_ord} ao ${ao}"

today = datetime.datetime.utcnow().replace(
            tzinfo=datetime.timezone.utc).astimezone(
                tz=pytz.timezone("US/Central")).strftime('%Y-%m-%d')

class TestTotalPosts(unittest.TestCase):
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
                ('Doogie', 'ao-golem', 1, '2022-12-04', 9, 'U257', '2022'),
                ('Doogie', 'ao-houseofpaine', 1, '2022-12-02', 9, 'U257', '2022'),
                ('Breach', 'ao-houseofpaine', 1, '2022-12-01', 9, 'U258', '2022')
            ]

            result = milestones.get(mock_conn, 'US/Central', template)

            assert len(result) == 1
            assert 'Name Doogie' in result[0]
            assert "<@U257>" in result[0] 
            assert "last_post 2022-12-04" in result[0]
            assert "ao_count 9" in result[0]
            assert "ao_count_ord 9th" in result[0]
            assert "ao ao-golem" in result[0]
            assert "2022" in result[0]

    @freeze_time('2022-12-04 14:00:00')
    def test_manyresults(self):
        with mock.patch('mysql.connector.connection') as mock_conn:
            cursor = mock.MagicMock()
            mock_conn.cursor.return_value = cursor
            cursor.fetchall.return_value = [
                ('Doogie', 'ao-golem', 1, '2022-12-04', 9, 'U257', '2022'),
                ('Doogie', 'ao-houseofpaine', 1, '2022-12-02', 9, 'U257', '2022'),
                ('Breach', 'ao-houseofpaine', 1, '2022-12-01', 9, 'U258', '2022'),
                ('Cheerio', 'ao-iditarod', 1, '2022-12-04', 9, 'U259', '2022')
            ]

            result = milestones.get(mock_conn, 'US/Central', template)

            assert len(result) == 2

            doogie =  list(filter(lambda r: 'U257' in r, result))[0]
            cheerio = list(filter(lambda r: 'U259' in r, result))[0]

            assert 'Name Doogie' in doogie
            assert "<@U257>" in doogie 
            assert "last_post 2022-12-04" in doogie
            assert "ao_count 9" in doogie
            assert "ao_count_ord 9th" in doogie
            assert "ao ao-golem" in doogie
            assert "2022" in doogie
            assert 'Name Cheerio' in cheerio
            assert "<@U259>" in cheerio 
            assert "last_post 2022-12-04" in cheerio
            assert "ao_count 9" in cheerio
            assert "ao_count_ord 9th" in cheerio
            assert "ao ao-iditarod" in cheerio
            assert "2022" in cheerio

        
if __name__ == 'main':
    unittest.main()