import datetime
import logging
import pytz
import string

def get(connection, local_timezone, post_template):
    sql = """   
        SELECT DATE_FORMAT( bi.date, '%Y-%m-%d' ) AS date, ao, q, pax_count, u.user_id as q_id
        FROM beatdown_info bi
        INNER JOIN (
            SELECT MAX(pax_count) max_pax_count 
            FROM beatdown_info bi2 
        ) s ON bi.pax_count = s.max_pax_count
        INNER JOIN users u 
        	ON u.user_name = bi.q
    """

    try:
        today = datetime.datetime.utcnow().replace(
            tzinfo=datetime.timezone.utc).astimezone(
                tz=pytz.timezone(local_timezone)).strftime('%Y-%m-%d')
        
        cursor = connection.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()

        if len(results) == 1:
            for row in results:
                date = row[0]
                ao = row[1]
                q = row[2]
                pax_count = row[3]
                q_id = row[4]

            if date == today:
                template_substitutes = dict(
                    ao = ao,
                    q = q,
                    q_tag = f"<@{q_id}>",
                    pax_count = pax_count
                )
                return [ string.Template(post_template).substitute(template_substitutes) ]
            else:
                return []
        else:
            return []

    except Exception as e:
        logging.error("Failure: " + str(e))