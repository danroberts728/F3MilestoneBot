import unittest
import unittest.mock as mock
import mysql.connector
from freezegun import freeze_time

import MilestoneTrigger.common as common
import MilestoneTrigger.config as config
import MilestoneTrigger.all_aos_milestone as aam

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

    # This is hacky, but we know Runner Up posted only once
    # at the Source on 10/7/2022. Since he moved to NC, he 
    # probably won't post there again even if he visits
    @freeze_time('2022-10-07 14:00:00')
    def test_sixpack_milestone(self):
        with mysql.connector.connect(
            host=db_host,
            database=db_database,
            user=db_username,
            password=db_password
        ) as connection:
            posts = aam.get(connection, 'US/Central', config.all_aos_milestone_template)

            assert len(posts) == 1
            assert 'U02C7AG2ZED' in posts[0]
        
if __name__ == 'main':
    unittest.main()