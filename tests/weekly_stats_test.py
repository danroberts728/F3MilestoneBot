import unittest
import unittest.mock as mock
from freezegun import freeze_time

import MilestoneTrigger.weekly_stats_milestone as milestones

template ="""Testing week_ending ${week_ending} 
    mon_count ${mon_count} 
    tue_count ${tue_count} 
    wed_count ${wed_count} 
    thu_count ${thu_count} 
    fri_count ${fri_count} 
    sat_count ${sat_count}
    max_week_count ${max_week_count}
    avg_week_count ${avg_week_count}
    this_week_count ${this_week_count}"""

sample_stats = [
    ('2022-01-03','1','161'),('2022-01-10','2','97'),('2022-01-17','3','145'),('2022-01-24','4','167'),('2022-01-31','5','152'),
    ('2022-02-07','6','155'),('2022-02-16','7','144'),('2022-02-23','8','116'),('2022-03-02','9','161'),('2022-03-07','10','147'),
    ('2022-03-16','11','134'),('2022-03-21','12','111'),('2022-03-28','13','140'),('2022-04-04','14','170'),('2022-04-11','15','163'),
    ('2022-04-20','16','168'),('2022-04-25','17','144'),('2022-05-04','18','157'),('2022-05-09','19','168'),('2022-05-16','20','117'),
    ('2022-05-23','21','123'),('2022-06-01','22','115'),('2022-06-06','23','124'),('2022-06-15','24','112'),('2022-06-20','25','102'),
    ('2022-06-27','26','100'),('2022-07-06','27','108'),('2022-07-13','28','124'),('2022-07-20','29','105'),('2022-07-25','30','134'),
    ('2022-08-03','31','148'),('2022-08-08','32','143'),('2022-08-15','33','181'),('2022-08-22','34','134'),('2022-08-29','35','160'),
    ('2022-09-07','36','129'),('2022-09-14','37','131'),('2022-09-19','38','129'),('2022-09-26','39','120'),('2022-10-05','40','141'),
    ('2022-10-10','41','113'),('2022-10-17','42','147'),('2022-10-26','43','128'),('2022-10-31','44','129'),('2022-11-07','45','126'),
    ('2022-11-16','46','106'),('2022-11-23','47','121'),('2022-11-28','48','107'),('2022-12-05','49','124'),('2022-12-12','50','120'),
    ('2022-12-19','51','106')]

sample_get_result = [('12/19/2022','Monday',24),('12/20/2022','Tuesday',13),('12/21/2022','Wednesday',22),('12/22/2022','Thursday',15),
    ('12/23/2022','Friday',23),('12/24/2022','Saturday',9)]

class TestWeeklyStats(unittest.TestCase):
    @freeze_time('2022-12-24 14:00:00')
    def test_stats(self):
        with mock.patch('mysql.connector.connection') as mock_conn:
            cursor = mock.MagicMock()
            mock_conn.cursor.return_value = cursor
            cursor.fetchall.return_value = sample_stats

            result = milestones.get_annual_max_avg(mock_conn, "US/Central")

            assert len(result) == 2
            assert result[0] == 181
            assert result[1] == 133.5

    @freeze_time('2022-12-24 14:00:00')
    def test_get(self):
        with mock.patch('mysql.connector.connection') as mock_conn:
            cursor = mock.MagicMock()
            mock_conn.cursor.return_value = cursor
            cursor.fetchall.return_value = sample_get_result

            result = milestones.get(mock_conn, "US/Central", (181, 133.5), template)

            assert len(result) == 1
            post = result[0]
            assert "week_ending Saturday, December 24, 2022" in post
            assert "mon_count 24" in post
            assert "tue_count 13" in post
            assert "wed_count 22" in post
            assert "thu_count 15" in post
            assert "fri_count 23" in post
            assert "sat_count 9" in post
            assert "max_week_count 181" in post
            assert "avg_week_count 133.5" in post
            assert "this_week_count 106" in post
        
if __name__ == 'main':
    unittest.main()