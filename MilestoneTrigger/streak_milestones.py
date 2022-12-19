import datetime
import logging
import pytz
import common

def get(connection, divisor, local_timezone):
    sql = f"""           
        WITH workouts AS (
            SELECT 
                s.date,
                ROW_NUMBER() OVER ( ORDER BY s.date ) AS workout_num
            FROM (
                SELECT DISTINCT 
                    bi.date
                FROM beatdown_info bi
                WHERE DAYOFWEEK(bi.date) != 1 # Always ignore Sundays
                ORDER BY bi.date
            ) s
        ),
        pax_posts AS (
            SELECT 
                s.pax,
                s.date,
                ROW_NUMBER() OVER ( PARTITION BY pax ORDER BY date ) AS pax_post_num
            FROM (
                # Have to do this because people do have 2 posts in a single day
                SELECT DISTINCT av.pax, av.date
                FROM attendance_view av
            ) s
            ORDER BY s.pax, s.date
        ),
        streak_groups AS (
            SELECT p.pax, p.date, wo.workout_num, p.pax_post_num,
                wo.workout_num - p.pax_post_num AS group_id
            FROM pax_posts p
            INNER JOIN workouts wo
                ON p.date = wo.date
        ),
        streaks AS (
            SELECT g.pax, g.date, g.workout_num, g.pax_post_num, group_id,
                ROW_NUMBER() OVER ( PARTITION BY pax, group_id ORDER BY date) AS streak_count
            FROM streak_groups g
        )
        SELECT pax, group_id, MAX(streak_count) as streak, MAX(date) as last_post, u.user_id
        FROM streaks
        INNER JOIN users u
	        ON u.user_name = streaks.pax
        WHERE streak_count > 1
        GROUP BY pax, group_id
        HAVING streak >= {divisor}
        ORDER BY pax, MAX(date) DESC
    """

    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()

        today = datetime.datetime.utcnow().replace(
            tzinfo=datetime.timezone.utc).astimezone(
                tz=pytz.timezone(local_timezone)).strftime('%Y-%m-%d')

        eligible_rows = list(filter(lambda r: r[2]%divisor == 0 and r[3] == today, results))

        retval = []

        for row in eligible_rows:
            ordinal_streak = common.make_ordinal(row[2])
            retval.append(f"{row[2]}-Day Streak! <@{row[4]}> is on fire with his {ordinal_streak} post in a row.")

        return retval
    except Exception as e:
        logging.error("Failure: " + str(e))