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
        WITH q_counts AS (
            SELECT
                bi.q,
                bi.ao, 
                COUNT(bi.ao) as num_qs,
                DATE_FORMAT( MAX(bi.date), '%Y-%m-%d' ) AS last_q
            FROM beatdown_info bi 
            WHERE bi.ao != 'ao-downrange' 
                AND bi.date BETWEEN DATE_FORMAT('{date_now}', '%Y-01-01') AND '{date_now}'
            GROUP BY bi.q, ao 
            ORDER BY bi.q, ao
        ),
        unique_ao_qs_count AS (
            SELECT
                q, COUNT(num_qs) as unique_qs
                FROM q_counts
                GROUP BY q		
        )
        SELECT qc.q, qc.ao, qc.num_qs, qc.last_q, uaqc.unique_qs,
            u.user_id, DATE_FORMAT('{date_now}', '%Y') AS year
        FROM q_counts qc
        INNER JOIN unique_ao_qs_count uaqc
            ON qc.q = uaqc.q
        INNER JOIN users u 
            ON u.user_name = qc.q
        WHERE uaqc.unique_qs = (SELECT COUNT(ao) FROM aos WHERE backblast = 1 AND ao != 'ao-downrange')
            AND qc.num_qs = 1"""
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

        # The SQL query returns PAX who have Q'ed all AOs this year and have 1 AO they 
        # hav Q'ed only once
        # But this 1 Q might have been from 6 months ago, so we must filter to results
        # that were posted today, meaning they just Q'ed their final AO for the year
        eligible_rows = list(filter(lambda r: r[3] == today, results))

        for row in eligible_rows:
            template_substitutes = dict(
                pax = row[0],
                pax_tag = f"<@{row[5]}>",
                ao = row[1],
                last_q = row[3],
                unique_q_count = row[4],
                unique_q_count_ord = common.make_ordinal(row[4]),
                pax_id = row[5],
                current_year = row[6]
            )
            post = string.Template(post_template).substitute(template_substitutes)

            slack_posts.append(post)

        return list(slack_posts)
    except Exception as e:
        logging.error("Failure: " + str(e))