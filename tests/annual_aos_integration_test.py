import unittest
import unittest.mock as mock
import mysql.connector
from freezegun import freeze_time

import MilestoneTrigger.common as common
import MilestoneTrigger.config as config
import MilestoneTrigger.annual_aos_milestone as aam

import os
from dotenv import load_dotenv

load_dotenv()

db_host = os.environ['F3M_PAXMINER_DB_HOST']
db_database = os.environ['F3M_PAXMINER_DB_DATABASE']
db_username = os.environ['F3M_PAXMINER_DB_USERNAME']
db_password = os.environ['F3M_PAXMINER_DB_PASSWORD']
slack_api_token = os.environ['F3M_SLACK_API_TOKEN']
post_channel_id = os.environ['F3M_SLACK_POST_CHANNEL_ID']

class TestAnnualAosIntegration(unittest.TestCase):

    @freeze_time('2023-02-08 14:00:00')
    def test_annual_aos_milestone(self):
        # A little bit of a hack because we know Crafty hit his
        # final AO of the year on 2/8/2023 in the database 
        with mysql.connector.connect(
            pool_name="F3MilestoneBotPool",
            host=db_host,
            database=db_database,
            user=db_username,
            password=db_password
        ) as connection:
            posts = aam.get(connection, 'US/Central', config.annual_aos_milestone_template)

            assert len(posts) == 1
            assert 'U02FAHPF2R0' in posts[0]
        
if __name__ == 'main':
    unittest.main()