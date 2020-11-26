import sqlite3
from datetime import datetime, timedelta
import requests
import json


# Returns a list containing the positive values from today.
# Returns -1 if there is no data
def positive_today():
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    values = []

    with conn:
        c.execute(
            """SELECT positive FROM data WHERE id=(SELECT MAX(date_id) FROM date)"""
        )
        for item in c.fetchall():
            if item[0] == None:
                values.append(-1)
            else:
                values.append(item[0])
    conn.close()
    return values


# Returns a list containing the negative values from today.
# Returns -1 if there is no data
def negative_today():
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    values = []

    with conn:
        c.execute(
            """SELECT negative FROM data WHERE id=(SELECT MAX(date_id) FROM date)"""
        )
        for item in c.fetchall():
            if item[0] == None:
                values.append(-1)
            else:
                values.append(item[0])
    conn.close()
    return values


# Returns a list containing the death values from today.
# Returns -1 if there is no data
def death_today():
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    values = []

    current_date = datetime_to_int(datetime.now())
    with conn:
        c.execute(
            """SELECT positive FROM data WHERE id=(SELECT MAX(date_id) FROM date)"""
        )
        for item in c.fetchall():
            if item[0] == None:
                values.append(-1)
            else:
                values.append(item[0])
    conn.close()
    return values


# Returns a list containing the TotalTestResults values from today.
def total_test_today():
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    values = []

    with conn:
        c.execute(
            """SELECT positive, negative FROM data WHERE id=(SELECT MAX(date_id) FROM date)"""
        )
        for item in c.fetchall():
            values.append(item[0]+item[1])
    conn.close()
    return values


# Returns a list containing the recovered values from today.
# Returns -1 if there is no data
def recovered_today():
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    values = []

    with conn:
        c.execute(
            """SELECT recovered FROM data WHERE id=(SELECT MAX(date_id) FROM date)"""
        )
        for item in c.fetchall():
            if item[0] == None:
                values.append(-1)
            else:
                values.append(item[0])
    conn.close()
    return values


# Returns a list containing the hospitalized values from today.
# Returns -1 if there is no data
def hospitalized_today():
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    values = []

    with conn:
        c.execute(
            """SELECT hospitalized FROM data WHERE id=(SELECT MAX(date_id) FROM date)"""
        )
        for item in c.fetchall():
            if item[0] == None:
                values.append(-1)
            else:
                values.append(item[0])
    conn.close()
    return values


# Returns a list containing the state names from today.
def state_names():
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    values = []

    current_date = datetime_to_int(datetime.now())
    with conn:
        c.execute("SELECT name FROM state")
        for item in c.fetchall():
            values.append(item[0])
    conn.close()
    return values


# Returns a list containing the state abbreviations from today.
def state_abbreviations():
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    values = []

    current_date = datetime_to_int(datetime.now())
    with conn:
        c.execute("SELECT abbreviation FROM state")
        for item in c.fetchall():
            values.append(item[0])
    conn.close()
    return values


# Returns a list containing the state abbreviations from today.
def state_population():
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    values = []

    current_date = datetime_to_int(datetime.now())
    with conn:
        c.execute("SELECT population FROM state")
        for item in c.fetchall():
            values.append(item[0])
    conn.close()
    return values


# Updates database to include latest data from Covid Tracking Project
def update_database():
    try:
        api_request_state_current = requests.get(
            "https://covidtracking.com/api/v1/states/daily.json", timeout=3
        )
        api = json.loads(api_request_state_current.content)
        conn = sqlite3.connect("data.db")
        c = conn.cursor()
        current_date = datetime_to_int(datetime.now())

        c.execute("SELECT MAX(id), MAX(date_id) FROM date")
        latest_date, latest_date_id = c.fetchone()

        for item in api:

            if item["date"] > latest_date:
                c.execute("SELECT date_id FROM date WHERE id=:id",
                          {'id': item["date"]})
                # conn.commit()
                if c.fetchall() == []:
                    c.execute(
                        "INSERT INTO date VALUES (:id, :date_id)",
                        {
                            "id": item["date"], 
                            "date_id": int_days_difference(
                                item['date'], 
                                latest_date
                            ) + latest_date_id},
                    )
                    conn.commit()

                c.execute(
                    "SELECT date_id FROM date WHERE id = :id", {
                        "id": item["date"]}
                )
                date_id = c.fetchone()[0]
                # conn.commit()

                c.execute(
                    "SELECT id FROM state WHERE abbreviation = :abbreviation",
                    {"abbreviation": item["state"]},
                )
                state_id = c.fetchone()[0]
                # conn.commit()

                c.execute(
                    "INSERT INTO data VALUES (:id, :positive, :negative, :hospitalized, :death, :recovered, :pending, :state_id)",
                    {
                        "id": date_id,
                        "positive": item["positive"],
                        "negative": item["negative"],
                        "hospitalized": item["hospitalizedCumulative"],
                        "death": item["death"],
                        "recovered": item["recovered"],
                        "pending": item["pending"],
                        "state_id": state_id,
                    },
                )
                conn.commit()
            elif item["date"] == latest_date:
                c.execute(
                    """UPDATE data SET
                            positive=:positive,
                            negative=:negative,
                            hospitalized=:hospitalized,
                            death=:death,
                            recovered=:recovered,
                            pending=:pending
                            WHERE (SELECT date_id FROM date WHERE id=:id)=id
                                AND (SELECT id FROM state WHERE abbreviation=:abbreviation)=state_id""",
                    {
                        "positive": item["positive"],
                        "negative": item["negative"],
                        "hospitalized": item["hospitalizedCumulative"],
                        "death": item["death"],
                        "recovered": item["recovered"],
                        "pending": item["pending"],
                        "id": item["date"],
                        "abbreviation": item["state"],
                    },
                )
                conn.commit()
            else:
                break
        conn.close()

    except Exception as e:
        print(e)


# Converts the datetime given to an int
# date is a date in datetime form
# days is the number of days to add to the given date
# returns the new date in int form
def datetime_to_int(date, days=0):
    return int(
        "".join(str(date.date() + timedelta(hours=3, days=days)).split("-"))
    )


# Converts an int to a datetime
# date is a date in int form
# returns the date into an int.
def int_to_datetime(date):
    return datetime.strptime(str(date), '%Y%m%d')


# Returns the difference in days between two dates as an int.
def int_days_difference(date_1, date_2):
    return abs((int_to_datetime(date_1) - int_to_datetime(date_2)).days)
