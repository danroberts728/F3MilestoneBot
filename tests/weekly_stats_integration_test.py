import unittest
import unittest.mock as mock
import mysql.connector
from freezegun import freeze_time

import MilestoneTrigger.common as common
import MilestoneTrigger.config as config
import MilestoneTrigger.weekly_stats_milestone as wsm

import os
from dotenv import load_dotenv

load_dotenv()

db_host = os.environ['F3M_PAXMINER_DB_HOST']
db_database = os.environ['F3M_PAXMINER_DB_DATABASE']
db_username = os.environ['F3M_PAXMINER_DB_USERNAME']
db_password = os.environ['F3M_PAXMINER_DB_PASSWORD']
slack_api_token = os.environ['F3M_SLACK_API_TOKEN']
post_channel_id = os.environ['F3M_SLACK_POST_CHANNEL_ID']

class TestWeeklyStatsIntegration(unittest.TestCase):

    # This is a bit of a hack because we know
    # our database state at this time
    @freeze_time('2022-12-24 14:00:00')
    def test_weekly_stats_milestone(self):
        with mysql.connector.connect(
            pool_name="F3MilestoneBotPool",
            host=db_host,
            database=db_database,
            user=db_username,
            password=db_password
        ) as connection:
            stats = wsm.get_annual_max_avg(connection, "US/Central")
            posts = wsm.get(connection, "US/Central", stats, config.weekly_stats_milestone_template)

            assert len(posts) == 1
            p = posts[0]
            assert "week ending Saturday, December 24, 2022" in p
            assert "Monday: 21" in p
            assert "Tuesday: 13" in p
            assert "Wednesday: 22" in p
            assert "Thursday: 15" in p
            assert "Friday: 23" in p
            assert "Saturday: 9" in p
            assert "Total: 103" in p
        
if __name__ == 'main':
    unittest.main()