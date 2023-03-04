import datetime
import pytz
import common
import logging
import string

def get(connection, number, local_timezone, post_template):
    sql = f"""  
        SELECT
            u.user_name AS pax, COUNT(u.user_id) as num_qs, 
            MAX(b.bd_date) as last_q,
            ROW_NUMBER() OVER ( ORDER BY COUNT(u.user_id) DESC) AS rnk,
            u.user_id,
            DATE_FORMAT(NOW(), '%Y') AS year
        FROM beatdowns b 
        INNER JOIN users u 
            ON b.q_user_id = u.user_id
        INNER JOIN aos a 
            ON b.ao_id = a.channel_id
        WHERE b.bd_date BETWEEN DATE_FORMAT(NOW(), '%Y-01-01') AND NOW()
            AND a.ao != 'ao-downrange'
        GROUP BY u.user_name
        ORDER BY COUNT(u.user_id) DESC"""

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

        eligible_rows = list(filter(lambda r: r[1] == number and r[2] == today, results))

        for row in eligible_rows:
            template_substitutes = dict(
                pax = row[0],
                qs_num = row[1],
                qs_ord = common.make_ordinal(row[1]),
                last_q = row[2],
                rank_num = row[3],
                rank_ord = common.make_ordinal(row[3]),
                pax_tag = f"<@{row[4]}>",
                current_year = row[5]
            )
            
            post = string.Template(post_template).substitute(template_substitutes)
            slack_posts.append(post)

        return list(slack_posts)
    except Exception as e:
        logging.error("Failure: " + str(e))