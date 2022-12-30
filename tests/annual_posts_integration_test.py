import unittest
import mysql.connector

import MilestoneTrigger.common as common
import MilestoneTrigger.config as config
import MilestoneTrigger.annual_posts_milestones as apm

import os
from dotenv import load_dotenv

load_dotenv()

db_host = os.environ['F3M_PAXMINER_DB_HOST']
db_database = os.environ['F3M_PAXMINER_DB_DATABASE']
db_username = os.environ['F3M_PAXMINER_DB_USERNAME']
db_password = os.environ['F3M_PAXMINER_DB_PASSWORD']
slack_api_token = os.environ['F3M_SLACK_API_TOKEN']
post_channel_id = os.environ['F3M_SLACK_POST_CHANNEL_ID']

class TestAnnualPostsIntegration(unittest.TestCase):
    # We will use the mode of the number of posts so
    # we have the highest probability of getting multiple 
    # posts at once.
    posts_number_mode: 0

    def test_annualpost_milestone(self):
        with mysql.connector.connect(
            pool_name="F3MilestoneBotPool",
            host=db_host,
            database=db_database,
            user=db_username,
            password=db_password
        ) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT pax, COUNT(pax) AS posts, MAX(date) AS last_post
                FROM attendance_view av 
                WHERE av.date BETWEEN DATE_FORMAT(NOW(), '%Y-01-01') AND NOW()
                GROUP BY pax
                HAVING last_post = CURDATE();""")
            result = list( cursor.fetchall() )
            if len(result) == 0:
                return
            just_counts = list( map(lambda x: x[1], result) )
            posts_number_mode = max(set(just_counts), key=just_counts.count)
            expected_length = len( list( filter(lambda r: r[1] == posts_number_mode, result) ) )

            posts = apm.get(connection, posts_number_mode, 'US/Central', config.annual_post_milestone_template, False)

            assert len(posts) == expected_length
            for p in posts:
                assert str(posts_number_mode) in p
                assert common.make_ordinal(posts_number_mode) in p
        
if __name__ == 'main':
    unittest.main()