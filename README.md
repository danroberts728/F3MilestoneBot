# F3MilestoneBot

The F3MilestoneBot is an Azure Function that reads an F3 PAXMiner database and posts certain PAX milestones. There are currently three types of milestones:

#### Total Posts Milestones
This recongizes PAX that have reached a certain number of total posts. The number of posts are configurable. For example, the total posts can be 10 and 100. Once any PAX reaches that number of posts, the app will post a message stating: "10 posts! Congratulations to @Crafty for making his 10th post to F3 Beast. He is the 81st PAX to reach this milestone."

The text of the post in this milestone and others is currently hard-coded.

#### Streak Milestones
This recognizes PAX that have posted a certain number of days in a row. You can configure the divisor. For example, the divisor can be set to 10. Once any PAX reaches his 10th, 20th, 30th etc. post in a row, the app will post a message stating: "20-Day Streak! @Crafty is on fire with his 20th post in a row."

The app will always skip Sundays and any day without a backblast posted when determining streaks.

#### Six Pack Milestones
This recognizes PAX that have posted 6 days in a row in a given week. It is only posted on Sundays for the previous week. Unlike the other milestones, this is a group post on slack. For example, it may read: "6-Pack Alert! T-Claps to @Crafty, @Eskimo and @Cheerio for posting every day last week."

To install:
- Rename config_sample.py to config.py
- Update the values in the config file as needed (below will help guide you)

## Database setup
This app assumes you have a standard F3 database setup for PAXMiner. Your db_host, db_database, db_username, and db_password should match the values you use for PAXMiner or to browse the database with a tool like DBeaver.

## Timezone considerations
The app uses pytz to set the local time in the app. You can get a list of all possible timezone values with pytz.all_timezones in Python. There are 595 possible values. Some US values include: 'US/Alaska', 'US/Aleutian', 'US/Arizona', 'US/Central', 'US-East-Indiana', 'US/Eastern', 'US/Hawaii', 'US/Indiana-Starke', 'US/Michigan', 'US/Mountain', 'US/Pacific', and 'US/Samoa'.

The config value 'local_timezone' should be one of the 595 pytz timezone values.

However, the app is also scheduled to run once a day within the MilestoneTrigger/function.json file. In this file, the cron-style scheduler is usually in UTC time unless you set up Azure to use a local timezone. 

## Slack
The slack_api_token in the config file is the token for your Slack app. Your app must have the chat:write scope.

The post_channel_id in the config file is the ID for the channel that Milestone posts will write to. This is *not* the name of the channel. The easiest way to discover the channel ID is to open Slack with a web browser and navigate to the channel. When the channel is up, the URL will be in the format https://app.slack.com/client/{workspace_id}/{channel_id}.

The minutes_between_posts in the config file is important when there are multiple milestones that are met in a single day. This sets a delay between posts.
