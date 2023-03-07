import datetime
import logging
import mysql.connector
import sys, os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))
import config
import total_posts_milestones as tpm
import streak_milestones as sm
import sixpack_milestones as spm
import annual_aos_milestone as aom
import max_attendance_milestone as mam
import weekly_stats_milestone as wsm
import annual_posts_milestones as apm
import annual_qs_milestone as aqm

import azure.functions as func

load_dotenv()

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    # Consume environment variables
    db_host = os.environ['F3M_PAXMINER_DB_HOST']
    db_database = os.environ['F3M_PAXMINER_DB_DATABASE']
    db_username = os.environ['F3M_PAXMINER_DB_USERNAME']
    db_password = os.environ['F3M_PAXMINER_DB_PASSWORD']
    slack_api_token = os.environ['F3M_SLACK_API_TOKEN']
    post_channel_id = os.environ['F3M_SLACK_POST_CHANNEL_ID']

    # Get Slack posts
    posts = []
    try:
        with mysql.connector.connect(
            host=db_host,
            database=db_database,
            user=db_username,
            password=db_password
        ) as connection:

            # Weekly Stats
            if config.use_weekly_stats_milestone:
                annual_stats = wsm.get_annual_max_avg(connection, config.local_timezone)
                weekly_stats_posts = wsm.get(connection, config.local_timezone, annual_stats, config.weekly_stats_milestone_template)
                posts += weekly_stats_posts
                logging.info(f"Weekly Stats milestone generated {len(weekly_stats_posts)} Slack posts.")

            # Annual Posts
            if config.use_annual_posts_milestone:
                for num in config.annual_post_milestone_numbers:
                    annual_posts_posts = apm.get(connection, num, config.local_timezone,config.annual_post_milestone_template, True)
                    posts += annual_posts_posts
                    logging.info(f"Annual Posts milestone generated {len(annual_posts_posts)} Slack posts.")

            # Total Posts
            if config.use_total_posts_milestone:
                for num in config.total_post_milestone_numbers:
                    total_posts_posts = tpm.get(connection, num, config.local_timezone, config.total_post_milestone_template)
                    posts += total_posts_posts
                    logging.info(f"Total Posts milestone generated {len(total_posts_posts)} Slack posts.")

            # Streaks
            if config.use_streak_milestone:
                streak_posts = sm.get(connection, config.streak_divisor, config.local_timezone, config.streak_milestone_template)
                posts += streak_posts
                logging.info(f"Streaks Milestone generated {len(streak_posts)} Slack posts.")

            # 6-Pack Alert
            if config.use_six_pack_milestones:
                sixpack_posts = spm.get(connection, config.local_timezone, config.sixpack_milestone_template)
                posts += sixpack_posts
                logging.info(f"Sixpack Milestone generated {len(sixpack_posts)} Slack posts.")

            # Annual AOs
            if config.use_annual_aos_milestone:
                annual_aos_posts = aom.get(connection, config.local_timezone, config.annual_aos_milestone_template)
                posts += annual_aos_posts
                logging.info(f"All AOs Milestone generated {len(annual_aos_posts)} Slack posts.")
            
            # Max Attendance
            if config.use_max_attendance_milestone:
                max_att_posts = mam.get(connection, config.local_timezone, config.max_attendance_milestone_template)
                posts += max_att_posts
                logging.info(f"Max Attendance Milestone generated {len(max_att_posts)} Slack posts.")

            # Qs this year
            if config.use_annual_qs_milestone:
                for num in config.annual_qs_milestone_numbers:
                    annual_q_posts = aqm.get(connection, num, config.local_timezone, config.annual_qs_milestone_template)

    except Exception as err:
        logging.error("Failure: " + str(err))


    # Post slack posts on delay
    try:
        slack = WebClient(token=slack_api_token)
        # Add 30 seconds so it doesn't complain about scheduling in the past
        schedule_datetime = datetime.datetime.now() + datetime.timedelta(seconds=30)
        minutes_between_posts = datetime.timedelta(minutes=config.minutes_between_posts)
    
        for p in posts:
            # Schedule post
            result = slack.chat_scheduleMessage(
                channel=post_channel_id,
                text=p,
                post_at=int(schedule_datetime.timestamp())
            )
            schedule_datetime = schedule_datetime + minutes_between_posts
            
            # Log the result
            logging.info(result)

    except Exception as err:
        logging.error("Failure: " + str(err))

    logging.info('Python timer trigger function ran at %s', utc_timestamp)
