import unittest
import unittest.mock as mock
import mysql.connector

import MilestoneTrigger.common as common
import MilestoneTrigger.config as config

import os
from dotenv import load_dotenv

load_dotenv()

db_host = os.environ['F3M_PAXMINER_DB_HOST']
db_database = os.environ['F3M_PAXMINER_DB_DATABASE']
db_username = os.environ['F3M_PAXMINER_DB_USERNAME']
db_password = os.environ['F3M_PAXMINER_DB_PASSWORD']
slack_api_token = os.environ['F3M_SLACK_API_TOKEN']
post_channel_id = os.environ['F3M_SLACK_POST_CHANNEL_ID']

class TestDbConnection(unittest.TestCase):

    def test_connection(self):
        try:
            with mysql.connector.connect(
                host=db_host,
                database=db_database,
                user=db_username,
                password=db_password
            ) as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT CURDATE() FROM dual")
                result = list(cursor.fetchall())
            cursor.close
        except Exception as err:
            self.fail(str(err))
        
if __name__ == 'main':
    unittest.main()