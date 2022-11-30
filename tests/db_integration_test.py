import unittest
import unittest.mock as mock
import mysql.connector

import MilestoneTrigger.common as common
import MilestoneTrigger.config as config
import MilestoneTrigger.total_posts_milestones as tpm

class TestTotalPostsIntegration(unittest.TestCase):
    def test_connection(self):
        try:
            with mysql.connector.connect(
                host=config.db_host,
                database=config.db_database,
                user=config.db_username,
                password=config.db_password
            ) as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT CURDATE() FROM dual")
                result = list(cursor.fetchall())
            cursor.close
        except Exception as err:
            self.fail(str(err))

    def test_totalpost_milestone(self):
        with mysql.connector.connect(
            host=config.db_host,
            database=config.db_database,
            user=config.db_username,
            password=config.db_password
        ) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT pax, MAX(date) AS last_post, COUNT(pax) as cnt 
                FROM attendance_view av 
                GROUP BY pax HAVING last_post = CURDATE()""")
            result = list( cursor.fetchall() )
            just_counts = list( map(lambda x: x[2], result) )
            mode = max(set(just_counts), key=just_counts.count)
            expected_length = len( list( filter(lambda r: r[2] == mode, result) ) )

            posts = tpm.get(connection, mode)

            assert len(posts) == expected_length
            for p in posts:
                assert str(mode) in p
                assert common.make_ordinal(mode) in p
        
if __name__ == 'main':
    unittest.main()