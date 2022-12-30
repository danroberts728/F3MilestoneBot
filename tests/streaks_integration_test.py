import unittest
import unittest.mock as mock
import mysql.connector
from freezegun import freeze_time

import MilestoneTrigger.common as common
import MilestoneTrigger.config as config
import MilestoneTrigger.streak_milestones as sm

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

    # This is a bit of a hack because we know
    # our database had 2 people end a 10-day streak on 4-28
    @freeze_time('2022-04-28 14:00:00')
    def test_sixpack_milestone(self):
        with mysql.connector.connect(
            pool_name="F3MilestoneBotPool",
            host=db_host,
            database=db_database,
            user=db_username,
            password=db_password
        ) as connection:
            posts = sm.get(connection, 10, 'US/Central', config.streak_milestone_template)

            assert len(posts) == 2
            for p in posts:
                assert 'U02HEAULWJF' in p or 'U02HXSCRXNF' in p
        
if __name__ == 'main':
    unittest.main()