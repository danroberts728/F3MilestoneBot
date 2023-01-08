import datetime
import logging
import pytz
import string

def get(connection, local_timezone, post_template):
    date_now = datetime.datetime.utcnow().replace(
            tzinfo=datetime.timezone.utc).astimezone(
                tz=pytz.timezone(local_timezone)).strftime('%Y-%m-%d')
    sql = f"""   
        WITH last_week AS (
            SELECT DISTINCT
                ba.user_id, ba.date
            FROM bd_attendance ba 
            WHERE ba.date BETWEEN DATE_ADD('{date_now}', INTERVAL -6 DAY)
                AND DATE_ADD('{date_now}', INTERVAL -1 DAY)
            ORDER BY ba.user_id, ba.date
        )
        SELECT 
            u.user_name AS pax,
            lw.user_id,
            MIN(lw.date) AS start,
            MAX(lw.date) AS stop,
            COUNT(lw.user_id) AS streak
        FROM last_week lw
        INNER JOIN users u
            ON u.user_id = lw.user_id
        GROUP BY lw.user_id
        HAVING streak >= 6
        ORDER BY COUNT(lw.user_id) DESC"""

    all_tags = []

    try:
        today = datetime.datetime.utcnow().replace(
            tzinfo=datetime.timezone.utc).astimezone(
                tz=pytz.timezone(local_timezone)).strftime('%A')
        
        if today == 'Sunday':
            cursor = connection.cursor()
            cursor.execute(sql)
            results = cursor.fetchall()
            cursor.close()

            for row in results:
                all_tags.append(f"<@{row[1]}>")
            
            milestone_count = str(len(results))
            tag_snippet = ""
            if len(all_tags) > 2:
                tag_snippet = ', '.join(all_tags[:-1]) + ", and " + str(all_tags[-1])
            elif len(all_tags) == 2:
                tag_snippet = ' and '.join(all_tags)
            elif len(all_tags) == 1:
                tag_snippet = all_tags[0]
            
            if len(all_tags) == 0:
                return []
            else:
                template_substitutes = dict(
                    tag_snippet = tag_snippet,
                    milestone_count = milestone_count
                )
                return [ string.Template(post_template).substitute(template_substitutes) ]
        else:
            return []

    except Exception as e:
        logging.error("Failure: " + str(e))