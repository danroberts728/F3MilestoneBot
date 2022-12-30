import datetime
import pytz
import common
import logging
import string

def get(connection, number, local_timezone, post_template):
    sql = f"""
    SELECT 
        u.user_name AS pax,
        DATE_FORMAT(MAX(ba.date), '%Y-%m-%d') AS last_post,
        COUNT(u.user_name) AS total_posts,
        ROW_NUMBER() OVER ( ORDER BY COUNT(u.user_name) DESC) AS rnk,
        u.user_id
    FROM bd_attendance ba 
    INNER JOIN users u 
        ON u.user_id = ba.user_id 
    GROUP BY u.user_name
    HAVING total_posts >= {number}
    ORDER BY COUNT(u.user_name) DESC"""

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
            template_substitutes = dict(
                pax = row[0],
                last_post = row[1],
                posts_num = row[2],
                rank_num = row[3],
                pax_id = row[4],
                pax_tag = f"<@{row[4]}>",
                posts_ord = common.make_ordinal(row[2]),
                rank_ord = common.make_ordinal(row[3])
            )
            

            post = string.Template(post_template).substitute(template_substitutes)
            slack_posts.append(post)

        return list(slack_posts)
    except Exception as e:
        logging.error("Failure: " + str(e))