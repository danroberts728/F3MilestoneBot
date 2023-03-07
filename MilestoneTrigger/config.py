### Region name. This is only used in the post templates in this file 
f3_region = "F3 Beast"

### Total Posts Milestone Settings
use_total_posts_milestone = False
total_post_milestone_numbers = [25, 50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]

### Annual Posts Milestone Settings
use_annual_posts_milestone = True
disable_annual_posts_for_first_year = False
annual_post_milestone_numbers = [25, 50, 100, 150, 200, 223, 250, 300, 325, 350]

### Streak Milestone Settings
use_streak_milestone = True
streak_divisor = 10

### Six Pack Milestone Settings
use_six_pack_milestones = True

### Annual All AOs Milestone Settings (per year)
use_annual_aos_milestone = True

### Max Attendence Milestone Settings
use_max_attendance_milestone = True

### Annual Qs Milestone Settings
use_annual_qs_milestone = True
annual_qs_milestone_numbers = [6, 12, 23, 24, 52]

### Weekly Stats Milestone Settings
use_weekly_stats_milestone = True

### Timezone Settings
local_timezone = "US/Central"

minutes_between_posts = 15

### Post Templates

# Available tags for Total Posts:
# ${pax}: The name of the PAX. This will not be tagged
# ${last_post}: The date of the last PAX's post, which should always be the current date, in YYYY-MM-DD format
# ${posts_num}: The total number of posts for the PAX (i.e. 50)
# ${pax_tag}: A tag for the post that will be a link to the user (i.e. @Ethanol)
# ${post_ord}: An ordinal version of the number of posts for the PAX (i.e. 50th)
# ${rank_num}: The rank of the PAX reaching this milestone. (i.e. 39)
# ${rank_ord}: The ordinal version of the rank fo the PAX reaching this milestone (i.e. 39th)
total_post_milestone_template = "${posts_num} lifetime posts! Congratulations to ${pax_tag} for making his ${posts_ord} post. He is the ${rank_ord} PAX to reach this milestone."

# Available tags for Six Pack:
# ${milestone_count}: The number of PAX who reached the milestone this week (i.e. 3)
# ${tag_snippet}: A tagged list of the PAX who reached the milestone this week (i.e. "Crafty, Dredd, and Spit Valve"
#   or "Crafty and Spit Valve" or just "Spit Valve")
sixpack_milestone_template = "6-Pack Alert! T-Claps to ${tag_snippet} for posting every day last week."

# Available tags for Streaks:
# ${pax}: The name of the PAX. This will not be tagged
# ${streak_count}: The number of posts in the current streak (i.e. 10)
# ${streak_count_ord}: THe ordinal versino fo the number of posts in the current streak (i.e. 10th)
# ${last_post}: The date of the last PAX's post, which should always be the current date, in YYYY-MM-DD format
# ${pax_tag}: A tag for the post that will be a link to the user (i.e. @Ethanol)
streak_milestone_template = "${streak_count}-Day Streak! ${pax_tag} is on fire with his ${streak_count_ord} post in a row."

# Available tags for Streaks:
# ${pax}: The name of the PAX. This will not be tagged
# ${last_post}: The date of the last PAX's post, which should always be the current date, in YYYY-MM-DD format
# ${pax_tag}: A tag for the post that will be a link to the user (i.e. @Ethanol)
# ${ao_count}: The number of AOs the PAX has been to (also the total number of AOs)
# ${ao_count_ord}: The ordinal version of the AO count (i.e. 9th)
# ${ao}: The AO that they just hit to get all the AOs
# ${year}: The current year
annual_aos_milestone_template = "${year} " + f3_region + " Traveler! ${pax_tag} has now posted at all ${ao_count} AOs in the region this year."

# Available tags for Max Attendance:
# ${ao}: The AO with the max attendance record for the day
# ${q}: The name of the Q. This will not be tagged.
# ${q_tag}: A tag for the slack post that will be a link to the Q (i.e. @Ethanol)
# ${pax_count}: The number of PAX at the workout
max_attendance_milestone_template = "New Attendance Record! ${q_tag} just Q'ed a workout attendance record for " + f3_region + " with @{pax_count} PAX at #{ao}"

# Available tags for Annual Posts:
# ${pax}: The name of the PAX. This will not be tagged
# ${last_post}: The date of the last PAX's post, which should always be the current date, in YYYY-MM-DD format
# ${posts_num}: The number of posts for the PAX in the current year (i.e. 50)
# ${pax_tag}: A tag for the post that will be a link to the user (i.e. @Ethanol)
# ${posts_ord}: An ordinal version of the number of posts for the PAX in the current year (i.e. 50th)
# ${posts_weekly_avg}: The number of posts per week on average this year (i.e. 3.4)
# ${current_year}: The current year
annual_post_milestone_template = "${posts_num} posts in ${current_year}! ${pax_tag} just made his ${posts_ord} post to " + f3_region + " this year."

# Available tags for Annual Qs:
# ${pax}: The name of the PAX. This will not be tagged
# ${qs_num}: The total number of posts for the PAX (i.e. 6)
# ${qs_ord}: The ordinal version of the Q count (i.e. 6th)
# ${last_q}: The date of the PAX's last Q, which should always be the curent date, in YYYY-MM-DD format
# ${rank_num}: The rank of the PAX reaching this milestone. (i.e. 39)
# ${rank_ord}: The ordinal version of the rank fo the PAX reaching this milestone (i.e. 39th)
# ${pax_tag}: A tag for the post that will be a link to the user (i.e. @Ethanol)
# ${current_year}: The current year
annual_qs_milestone_template = "${qs_num} Qs in ${current_year}! ${pax_tag} just Qed his ${qs_ord} workout for " + f3_region + " this year."


# Available tags for Weekly Stats:
# ${week_ending}: The Saturday ending the week in <day>, <month> <date>, <year> format (i.e. Saturday, December 24, 2022)
# ${this_week_count}: Number of posts this week (should be sum of the day counts below)
# ${mon_count}: The post count for Monday
# ${tue_count}: The post count for Tuesday
# ${wed_count}: The post count for Wednesday
# ${thu_count}: The post count for Thursday
# ${fri_count}: The post count for Friday
# ${sat_count}: The post count for Saturday
# ${max_week_count}: The max weekly post count for the current year
# ${avg_week_count}: The average weekly post count for the current year
weekly_stats_milestone_template = f3_region + """ posting summary for the week ending ${week_ending}:

Monday: ${mon_count}
Tuesday: ${tue_count}
Wednesday: ${wed_count}
Thursday: ${thu_count}
Friday: ${fri_count}
Saturday: ${sat_count}
*Total: ${this_week_count}*

Biggest count this year: ${max_week_count}
Average count this year: ${avg_week_count}"""