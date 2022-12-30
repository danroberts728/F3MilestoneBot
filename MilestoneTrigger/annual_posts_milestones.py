import datetime
import pytz
import common
import logging
import string

def get(connection, number, local_timezone, post_template, disable_annual_posts_for_first_year = True):
    sql = f"""  
        SELECT 
            av.pax, 
            COUNT(av.pax) AS posts, 
            COUNT(av.pax)/CEILING(DAYOFYEAR(SYSDATE())/7) AS weekly_avg,
            DATE_FORMAT( MAX(av.date), '%Y-%m-%d') AS last_post,
            first_posts.year AS first_post_year,
            u.user_id 
        FROM attendance_view av 
        INNER JOIN users u
            ON av.pax = u.user_name
        INNER JOIN (
        	SELECT ba.user_id, DATE_FORMAT(MIN(ba.date), '%Y') AS year
        	FROM bd_attendance ba
        	GROUP BY ba.user_id
        ) first_posts ON first_posts.user_id = u.user_id
        WHERE av.date BETWEEN DATE_FORMAT(NOW(), '%Y-01-01') AND NOW()
        GROUP BY pax
        HAVING posts >= {number}
        ORDER BY COUNT(pax) DESC;"""

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

        current_year = datetime.datetime.utcnow().replace(
            tzinfo=datetime.timezone.utc).astimezone(
                tz=pytz.timezone(local_timezone)).strftime('%Y')

        eligible_rows = list(filter(lambda r: r[1] == number and r[3] == today, results))
        if disable_annual_posts_for_first_year:
            eligible_rows = list(filter(lambda r: r[4] == current_year, eligible_rows))

        for row in eligible_rows:
            template_substitutes = dict(
                pax = row[0],
                posts_num = row[1],
                posts_ord = common.make_ordinal(row[1]),
                posts_weekly_avg = row[2],
                last_post = row[3],
                pax_tag = f"<@{row[5]}>",
                current_year = current_year
            )
            
            post = string.Template(post_template).substitute(template_substitutes)
            slack_posts.append(post)

        return list(slack_posts)
    except Exception as e:
        logging.error("Failure: " + str(e))