import unittest
import unittest.mock as mock
import mysql.connector
from freezegun import freeze_time

import MilestoneTrigger.common as common
import MilestoneTrigger.config as config
import MilestoneTrigger.max_attendance_milestone as mam

import os
from dotenv import load_dotenv

load_dotenv()

db_host = os.environ['F3M_PAXMINER_DB_HOST']
db_database = os.environ['F3M_PAXMINER_DB_DATABASE']
db_username = os.environ['F3M_PAXMINER_DB_USERNAME']
db_password = os.environ['F3M_PAXMINER_DB_PASSWORD']
slack_api_token = os.environ['F3M_SLACK_API_TOKEN']
post_channel_id = os.environ['F3M_SLACK_POST_CHANNEL_ID']

class TestSixPackIntegration(unittest.TestCase):

    # This is a bit of a hack that will fail at some point,
    # but we have a max attendance record with Hammy that has stood
    # for a while
    @freeze_time('2022-01-28 14:00:00')
    def test_max_attedance(self):
        with mysql.connector.connect(
            pool_name="F3MilestoneBotPool",
            host=db_host,
            database=db_database,
            user=db_username,
            password=db_password
        ) as connection:
            posts = mam.get(connection, 'US/Central', config.max_attendance_milestone_template)

            assert len(posts) == 1
            for p in posts:
                assert 'U02B5JT7R53' in p
        
if __name__ == 'main':
    unittest.main()