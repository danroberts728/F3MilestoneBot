import datetime
import logging
import pytz
import string

def get(connection, local_timezone, annual_stats, weekly_unique_count, post_template):
    date_now = datetime.datetime.utcnow().replace(
            tzinfo=datetime.timezone.utc).astimezone(
                tz=pytz.timezone(local_timezone)).strftime('%Y-%m-%d')
    sql = f"""
    SELECT 
        DATE_FORMAT(bi.date,'%Y-%m-%d') AS date, 
        DATE_FORMAT(bi.date,'%W') as day,
        SUM(bi.pax_count) AS cnt
    FROM beatdown_info bi
    WHERE bi.ao != 'ao-downrange' 
        AND bi.date 
            BETWEEN DATE_ADD('{date_now}', INTERVAL -6 DAY) AND '{date_now}'

    GROUP BY bi.date
    ORDER BY bi.date;"""
    
    try:
        today = datetime.datetime.utcnow().replace(
            tzinfo=datetime.timezone.utc).astimezone(
                tz=pytz.timezone(local_timezone)).strftime('%A')
        
        if today == 'Saturday':
            cursor = connection.cursor()
            cursor.execute(sql)
            results = cursor.fetchall()
            cursor.close()

            weekly_total = sum(list(map(lambda x: x[2], results)))

            if(weekly_total > annual_stats[0]):
                max_weekly_count = weekly_total
            else:
                max_weekly_count = annual_stats[0]
            avg_weekly_count = annual_stats[1]

            monday_data = list( filter(lambda x: x[1] == 'Monday', results) )
            tuesday_data = list( filter(lambda x: x[1] == 'Tuesday', results) )
            wednesday_data = list( filter(lambda x: x[1] == 'Wednesday', results) )
            thursday_data = list( filter(lambda x: x[1] == 'Thursday', results) )
            friday_data = list( filter(lambda x: x[1] == 'Friday', results) )
            saturday_data = list( filter(lambda x: x[1] == 'Saturday', results) )

            monday_count = monday_data[0][2] if len(monday_data) == 1 else 0
            tuesday_count = tuesday_data[0][2] if len(tuesday_data) == 1 else 0
            wednesday_count = wednesday_data[0][2] if len(wednesday_data) == 1 else 0
            thursday_count = thursday_data[0][2] if len(thursday_data) == 1 else 0
            friday_count = friday_data[0][2] if len(friday_data) == 1 else 0
            saturday_count = saturday_data[0][2] if len(saturday_data) == 1 else 0

            template_substitutes = dict(
                week_ending = datetime.datetime.utcnow().replace(
                    tzinfo=datetime.timezone.utc).astimezone(
                        tz=pytz.timezone(local_timezone)).strftime("%A, %B %e, %Y").replace('  ', ' '),
                mon_count = monday_count,
                tue_count = tuesday_count,
                wed_count = wednesday_count,
                thu_count = thursday_count,
                fri_count = friday_count,
                sat_count = saturday_count,
                this_week_count = weekly_total,
                max_week_count = max_weekly_count,
                avg_week_count = avg_weekly_count,
                weekly_unique_count = weekly_unique_count
            )
            return [ string.Template(post_template).substitute(template_substitutes) ]


        else:
            return []

    except Exception as e:
        logging.error("Failure: " + str(e))


def get_weekly_unique(connection, local_timezone):
    date_now = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).astimezone(
            tz=pytz.timezone(local_timezone)).strftime('%Y-%m-%d')
    sql_unique = f"""
    SELECT COUNT(s.pax) AS unique_pax
    FROM (
        SELECT pax, COUNT(pax)
        FROM attendance_view av 
        WHERE av.date 
            BETWEEN DATE_ADD('{date_now}', INTERVAL -6 DAY) AND '{date_now}'
            AND av.ao != 'ao-downrange'
        GROUP BY pax
    ) s 
    """    
    try:        
        cursor = connection.cursor()
        cursor.execute(sql_unique)
        results = cursor.fetchall()
        cursor.close()

        return results[0][0]

    except Exception as e:
        logging.error("Failure: " + str(e))
    

def get_annual_max_avg(connection, local_timezone):
    date_now = datetime.datetime.utcnow().replace(
            tzinfo=datetime.timezone.utc).astimezone(
                tz=pytz.timezone(local_timezone)).strftime('%Y-%m-%d')
    sql_stats = f"""   
        SELECT 
            DATE_FORMAT(bi.date, '%Y-%m-%d'), 
            WEEK(bi.date, 3) AS wk, 
            SUM(bi.pax_count)
        FROM beatdown_info bi
        WHERE bi.date 
            BETWEEN DATE_FORMAT('{date_now}', '%Y-01-01') AND '{date_now}'
            AND bi.ao != 'ao-downrange'
        GROUP BY WEEK(bi.date, 3)
        HAVING wk <= WEEK('{date_now}', 3) 
        ORDER BY WEEK(bi.date, 3);
    """

    try:
        cursor = connection.cursor()
        cursor.execute(sql_stats)
        results = cursor.fetchall()
        cursor.close()

        just_counts = list(map(lambda x: int(x[2]), results))
        avg_week = round( sum(just_counts) / len(just_counts), 1 )
        max_week = max(just_counts)

        return (max_week, avg_week)


    except Exception as e:
        logging.error("Failure: " + str(e))