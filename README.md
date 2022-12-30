# F3MilestoneBot [![Dev Tests](https://github.com/danroberts728/F3MilestoneBot/actions/workflows/dev_tests.yml/badge.svg)](https://github.com/danroberts728/F3MilestoneBot/actions/workflows/dev_tests.yml)

The F3MilestoneBot is an Azure Function that reads an F3 PAXMiner database and posts certain PAX milestones. There are currently three types of milestones:

#### Total Posts Milestones
This recongizes PAX that have reached a certain number of total posts. The number of posts are configurable. For example, the total posts can be 10 and 100. Once any PAX reaches that number of posts, the app will post a message stating: "10 posts! Congratulations to @Crafty for making his 10th post to F3 Beast. He is the 81st PAX to reach this milestone."

The text of the post in this milestone and others is currently hard-coded.

#### Streak Milestones
This recognizes PAX that have posted a certain number of days in a row. You can configure the divisor. For example, the divisor can be set to 10. Once any PAX reaches his 10th, 20th, 30th etc. post in a row, the app will post a message stating: "20-Day Streak! @Crafty is on fire with his 20th post in a row."

The app will always skip Sundays and any day without a backblast posted when determining streaks.

#### Six Pack Milestones
This recognizes PAX that have posted 6 days in a row in a given week. It is only posted on Sundays for the previous week. Unlike the other milestones, this is a group post on slack. For example, it may read: "6-Pack Alert! T-Claps to @Crafty, @Eskimo and @Cheerio for posting every day last week."

### Potential Future Milestones
#### _World Traveler Milestone_
This recognizes a PAX that has posted at every AO in the region.

#### _Q Traveler Milestones_
This recognizes a PAX that has Q'ed at every AO in the region.

#### _Max Attendance Milestone_
This posts when a workout that day is the largest workout in the history of the region.

#### _Total Men Led Milestones_
This posts when a PAX has led X number of PAX as the Q of a workout. The value of X is configurable. For example, the total men led can be 100 and 500. Once any PAX reaches that number of men led, the app will post a message.

#### _Annual Posts Milestones_
This recongizes PAX that have reached a certain number of posts in the current year. The number of posts are configurable. There is also a recommended configuration to turn off the milestone for PAX that are in their first year to prevent duplicates.

#### _Weekly Stats_ 
This is a weekly post that gives the stats for the week and compares it to the year. It can show the total posts, the breakdown by day, the average weekly posts for the year, the max posts per year, and an indication of whether the current week is a new record.

## Multiple milestones
In the event that there are multiple milestones in a single day, the app will schedule subsequent posts. The duration between posts is configurable.

## Known issues
The database queries rely on the views present in the default PAXMiner schema. Because of this, if a user_name (PAX name in Slack) has a duplicate, it will cause duplication issues with some milestones. To prevent this from causing issues, every PAX should have a unique user_name in Slack.

There is no persistence of data, which creates limitations. The main limitation is that the app does not know if it has already posted a milestone. In order to prevent duplicate posts, the app only runs once per day. This creates an issue - if the app is run before all backblasts are posted for the day, it will not "know" if a certain milestone has been met for that day. Then the next day, it will assume it was posted previously and not post it. 

In other words, all the day's backblasts must be posted before the app is run in order for it to post any milestones that were reached that day. The one exception to this is for the Six Pack milestone. For the Six Pack mlestone, all the previous week's backblasts must be posted before the app is run on the following Sunday.

## To install:
- Rename config_sample.py to config.py
- Update the values in the config file as needed (below will help guide you)

## Database setup
This app assumes you have a standard F3 database setup for PAXMiner. Your db_host, db_database, db_username, and db_password should match the values you use for PAXMiner or to browse the database with a tool like DBeaver.

## Timezone considerations
The app uses pytz to set the local time in the app. You can get a list of all possible timezone values with pytz.all_timezones in Python. There are 595 possible values. Some US values include: 'US/Alaska', 'US/Aleutian', 'US/Arizona', 'US/Central', 'US-East-Indiana', 'US/Eastern', 'US/Hawaii', 'US/Indiana-Starke', 'US/Michigan', 'US/Mountain', 'US/Pacific', and 'US/Samoa'.

The config value 'local_timezone' should be one of the 595 available pytz timezone values.

However, the app is also scheduled to run once a day within the MilestoneTrigger/function.json file. In this file, the cron-style scheduler is usually in UTC time unless you set up Azure to use a local timezone. 

## Slack
The slack_api_token in the config file is the token for your Slack app. Your app must have the chat:write scope.

The post_channel_id in the config file is the ID for the channel that Milestone posts will write to. This is *not* the name of the channel. The easiest way to discover the channel ID is to open Slack with a web browser and navigate to the channel. When the channel is up, the URL will be in the format https://app.slack.com/client/{workspace_id}/{channel_id}.

The minutes_between_posts in the config file is important when there are multiple milestones that are met in a single day. This sets a delay between posts.
