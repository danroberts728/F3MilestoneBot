import datetime
import logging
import mysql.connector
import sys, os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))
import config
import total_posts_milestones as tpm
import streak_milestones as sm
import sixpack_milestsones as spm

import azure.functions as func


def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    # Get Slack posts
    posts = []
    try:
        with mysql.connector.connect(
            host=config.db_host,
            database=config.db_database,
            user=config.db_username,
            password=config.db_password
        ) as connection:

            # Total Posts
            if config.use_total_posts_milestone:
                for num in config.total_post_milestone_numbers:
                    posts +=  tpm.get(connection, num)

            # Streaks
            if config.use_streak_milestone:
                posts += sm.get(connection, config.streak_divisor)

            # 6-Pack Alert
            if config.use_six_pack_milestones:
                posts += spm.get(connection)

    except Exception as err:
        logging.error("Failure: " + str(err))


    # Post slack posts on delay
    try:
        slack = WebClient(token=config.slack_api_token)
        # Add 30 seconds so it doesn't complain about scheduling in the past
        schedule_datetime = datetime.datetime.now() + datetime.timedelta(seconds=30)
        minutes_between_posts = datetime.timedelta(minutes=config.minutes_between_posts)
    
        for p in posts:
            # Schedule post
            result = slack.chat_scheduleMessage(
                channel=config.post_channel_id,
                text=p,
                post_at=int(schedule_datetime.timestamp())
            )
            schedule_datetime = schedule_datetime + minutes_between_posts
            
            # Log the result
            logging.info(result)

    except Exception as err:
        logging.error("Failure: " + str(err))

    logging.info('Python timer trigger function ran at %s', utc_timestamp)
