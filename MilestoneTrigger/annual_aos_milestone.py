import datetime
import pytz
import common
import logging
import string

def get(connection, local_timezone, post_template):
    date_now = datetime.datetime.utcnow().replace(
            tzinfo=datetime.timezone.utc).astimezone(
                tz=pytz.timezone(local_timezone)).strftime('%Y-%m-%d')
    sql = f"""
        WITH post_counts AS (
            SELECT
                av.pax, 
                av.ao, 
                COUNT(av.ao) as num_posts,
                DATE_FORMAT( MAX(av.date), '%Y-%m-%d' ) AS last_post
            FROM attendance_view av 
            WHERE ao != 'ao-downrange' 
            	AND av.date BETWEEN DATE_FORMAT('{date_now}', '%Y-01-01') AND '{date_now}'
            GROUP BY pax, ao 
            ORDER BY pax, ao
        ),
        unique_aos_count AS (
            SELECT
                pax, COUNT(num_posts) as unique_aos
                FROM post_counts
                GROUP BY pax		
        )
        SELECT pc.pax, pc.ao, pc.num_posts, pc.last_post, uac.unique_aos,
        	u.user_id, DATE_FORMAT('{date_now}', '%Y') AS year
        FROM post_counts pc
        INNER JOIN unique_aos_count uac
            ON pc.pax = uac.pax
        INNER JOIN users u 
        	ON u.user_name = pc.pax
        WHERE uac.unique_aos = (SELECT COUNT(ao) FROM aos WHERE backblast = 1 AND ao != 'ao-downrange')
            AND pc.num_posts = 1"""
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

        # The SQL query returns PAX who have visited all AOs and have 1 post on at least one AO
        # But this 1 visit might have been from 6 years ago, so we must filter to results
        # that were posted today, meaning they just hit their final AO
        eligible_rows = list(filter(lambda r: r[3] == today, results))

        for row in eligible_rows:
            template_substitutes = dict(
                pax = row[0],
                pax_tag = f"<@{row[5]}>",
                ao = row[1],
                last_post = row[3],
                ao_count = row[4],
                ao_count_ord = common.make_ordinal(row[4]),
                pax_id = row[5],
                year = row[6]
            )
            post = string.Template(post_template).substitute(template_substitutes)

            slack_posts.append(post)

        return list(slack_posts)
    except Exception as e:
        logging.error("Failure: " + str(e))