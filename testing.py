import sqlite3
from datetime import datetime, timedelta
import requests
import json

# Updates database to include latest
def update_database():
    try:
        api_request_state_current = requests.get(
            "https://covidtracking.com/api/v1/states/daily.json", timeout=3
        )
        api = json.loads(api_request_state_current.content)
        conn = sqlite3.connect("temp.db")
        c = conn.cursor()
        current_date = current_datetime()

        c.execute("SELECT id FROM date WHERE (SELECT MAX(date_id) from date) = date_id")
        latest_date = c.fetchone()[0]
        conn.commit()
        for item in api:

            if item["date"] == latest_date:
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
                        "hospitalized": item["hospitalized"],
                        "death": item["death"],
                        "recovered": item["recovered"],
                        "pending": item["pending"],
                        "id": item["date"],
                        "abbreviation": item["state"],
                    },
                )
                conn.commit()
            # Insert new date and data values
            elif item["date"] > latest_date:
                c.execute(
                    "INSERT INTO date VALUES (:id, :date_id)",
                    {"id": item["date"], "date_id": counter},
                )
                conn.commit()
                c.execute(
                    "SELECT date_id FROM date WHERE id = :id", {"id": item["date"]}
                )
                date_id = c.fetchall()[0][0]
                conn.commit()
                c.execute(
                    "SELECT id FROM state WHERE abbreviation = :abbreviation",
                    {"abbreviation": item["state"]},
                )
                state_id = c.fetchall()[0][0]

                c.execute(
                    "INSERT INTO data VALUES (:id, :positive, :negative, :hospitalized, :death, :recovered, :pending, :state_id)",
                    {
                        "id": date_id,
                        "positive": item["positive"],
                        "negative": item["negative"],
                        "hospitalized": item["hospitalized"],
                        "death": item["death"],
                        "recovered": item["recovered"],
                        "pending": item["pending"],
                        "state_id": state_id,
                    },
                )
            else:
                break

        conn.close()

    except Exception as e:
        print(e)


# Returns the current date
def current_datetime():
    return int(
        "".join(str(datetime.now().date() + timedelta(hours=3, days=-2)).split("-"))
    )


# Returns a list containing the positive values from today.
def positive_today():
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    positive_values = []

    current_date = current_datetime()
    with conn:
        c.execute(
            """SELECT positive FROM data WHERE (SELECT date_id FROM date WHERE id=:id)=id""",
            {"id": current_date},
        )
        for item in c.fetchall():
            positive_values.append(item[0])
    return positive_values


# update_database()
