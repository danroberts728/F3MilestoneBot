import datetime
import logging
import pytz
import string

def get(connection, local_timezone, post_template):
    sql = """   
        SELECT DISTINCT
            av.pax, u.user_id, MIN(av.date) as start, MAX(av.date) as stop, COUNT(av.pax) as streak
        FROM attendance_view av 
        INNER JOIN users u 
            ON u.user_name = av.pax
        INNER JOIN bd_attendance ba 
            ON u.user_id = ba.user_id
            AND av.date = ba.date
        WHERE av.date IN (
            SELECT DISTINCT bi.date
                FROM beatdown_info bi 
                WHERE bi.date BETWEEN DATE_ADD(CURDATE(), INTERVAL -6 DAY)
                        AND DATE_ADD(CURDATE(), INTERVAL -1 DAY)
                    AND DAYOFWEEK(bi.date) != 1
        )
        GROUP BY av.pax, u.user_id
        HAVING streak >= 6 
        	AND DAYOFWEEK(start) = 2 
        	AND DAYOFWEEK(stop) = 7
        ORDER BY COUNT(av.pax) DESC
    """

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