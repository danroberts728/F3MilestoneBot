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
        
if __name__ == 'main':
    unittest.main()