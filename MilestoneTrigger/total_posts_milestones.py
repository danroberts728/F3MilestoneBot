import datetime
import config
import pytz
import common
import logging

def get(connection, number, local_timezone):
    sql = f"""  SELECT 
                    av.pax, 
                    DATE_FORMAT( MAX(av.date), '%Y-%m-%d' ) AS last_post,
                    COUNT(av.pax) AS total_posts,
                    ROW_NUMBER() OVER ( ORDER BY COUNT(av.pax) DESC ) AS rnk,
                    u.user_id
                FROM attendance_view av 
                INNER JOIN users u 
                	ON u.user_name = av.pax
                GROUP BY av.pax 
                HAVING total_posts >= {number}
                ORDER BY COUNT(av.pax) DESC"""

    try:
        slack_posts = []

        cursor = connection.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()

        # Today's date in the same format as the SQL result above
        today = datetime.datetime.utcnow().replace(
            tzinfo=datetime.timezone.utc).astimezone(
                tz=pytz.timezone(local_timezone)).strftime('%Y-%m-%d')

        eligible_rows = list(filter(lambda r: r[2] == number and r[1] == today, results))

        for row in eligible_rows:
            ordinal_posts = common.make_ordinal(row[2])
            ordinal_rank = common.make_ordinal(row[3])
            slack_posts.append(
                f"{number} posts! Congratulations to <@{row[4]}> for making his {ordinal_posts} post to F3 Beast. He is the {ordinal_rank} PAX to reach this milestone.")

        return list(slack_posts)
    except Exception as e:
        logging.error("Failure: " + str(e))