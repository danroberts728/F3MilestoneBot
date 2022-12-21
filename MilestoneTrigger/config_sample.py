### Region name. This is only used in the post templates in this file 
f3_region = "F3 Beast"

### Total Posts Milestone Settings
use_total_posts_milestone = True
total_post_milestone_numbers = [25, 50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]

### Streak Milestone Settings
use_streak_milestone = True
streak_divisor = 10

### Six Pack Milestone Settings
use_six_pack_milestones = True

### All AOs Milestone Settings
use_all_aos_milestone = True

### Database Settings
db_host = '<db_url>'
db_database = '<db_name>'
db_username = '<db_username'
db_password = '<db_password>'

### Timezone Settings
local_timezone = 'US/Central'

### Slack API Settings
slack_api_token = '<app_token>'
post_channel_id = '<channel_id>'
minutes_between_posts = 60

### Post Templates

# Available tags for Total Posts:
# ${pax}: The name of the PAX. This will not be tagged
# ${last_post}: The date of the last PAX's post, which should always be the current date, in YYYY-MM-DD format
# ${posts_num}: The total number of posts for the PAX (i.e. 50)
# ${pax_tag}: A tag for the post that will be a link to the user (i.e. @Ethanol)
# ${post_ord}: An ordinal version of the number of posts for the PAX (i.e. 50th)
# ${rank_num}: The rank of the PAX reaching this milestone. (i.e. 39)
# ${rank_ord}: The ordinal version of the rank fo the PAX reaching this milestone (i.e. 39th)
total_post_milestone_template = "${posts_num} posts! Congratulations to ${pax_tag} for making his ${post_ord} post to " + f3_region + ". He is the ${rank_ord} PAX to reach this milestone."

# Available tags for Six Pack:
# ${milestone_count}: The number of PAX who reached the milestone this week (i.e. 3)
# ${tag_snippet}: A tagged list of the PAX who reached the milestone this week (i.e. "Crafty, Dredd, and Spit Valve"
#   or "Crafty and Spit Valve" or just "Spit Valve")
sixpack_milestone_template = "6-Pack Alert! T-Claps to {tag_snippet} for posting every day last week."

# Available tags for Streaks:
# ${pax}: The name of the PAX. This will not be tagged
# ${streak_count}: The number of posts in the current streak (i.e. 10)
# ${streak_count_ord}: THe ordinal versino fo the number of posts in the current streak (i.e. 10th)
# ${last_post}: The date of the last PAX's post, which should always be the current date, in YYYY-MM-DD format
# ${pax_tag}: A tag for the post that will be a link to the user (i.e. @Ethanol)
streak_milestone_template = "${streak_count}-Day Streak! ${pax_tag} is on fire with his ${ordinal_streak} post in a row."

# Available tags for Streaks:
# ${pax}: The name of the PAX. This will not be tagged
# ${last_post}: The date of the last PAX's post, which should always be the current date, in YYYY-MM-DD format
# ${pax_tag}: A tag for the post that will be a link to the user (i.e. @Ethanol)
# ${ao_count}: The number of AOs the PAX has been to (also the total number of AOs)
# ${ao_count_ord}: The ordinal version of the AO count (i.e. 9th)
# ${ao}: The AO that they just hit to get all the AOs
all_aos_milestone_template = f3_region + " Traveler! ${pax_tag} has now posted at all ${ao_count} AOs in the region."