import sqlite3
import requests
import json


# Connect to Database

# conn = sqlite3.connect('data.db')

# c = conn.cursor()

# Grabs data from Covid Tracking Projects and hold the list in api

# api_request_state_current = requests.get(
#     "https://covidtracking.com/api/v1/states/daily.json", timeout=3)
# api = json.loads(api_request_state_current.content)


# Creating tables

# with conn:
#     c.execute("""CREATE TABLE date (
#             id integer,
#             date_id integer
#         )""")
# with conn:
#     c.execute("""CREATE TABLE data (
#             id integer,
#             positive integer,
#             negative integer,
#             hospitalized integer,
#             death integer,
#             recovered intger,
#             pending integer,
#             state_id intger
#         )""")

# with conn:
#     c.execute("""CREATE TABLE state (
#             id integer,
#             name text,
#             abbreviation text,
#             population integer
#         )""")


# Filling date table

# counter = 129
# for item in api:
#     if item['date'] >= 20200326:
#         c.execute("SELECT id FROM date WHERE id = :id", {'id': item['date']})
#         data = c.fetchall()
#         conn.commit()
#         if len(data) == 0:
#             c.execute("INSERT INTO date VALUES (:id, :date_id)",
#                       {'id': item['date'], 'date_id': counter})
#             conn.commit()
#             counter -= 1


# Filling state table

# p = open("USPopulation.txt", 'r')
# pop = json.loads(p.read())

# state_counter = 0
# for item in pop:
#     c.execute("INSERT INTO state VALUES (:id, :name, :abbreviation, :population)", {
#         'id': state_counter,
#         'name': item['state'],
#         'abbreviation': item['abb'],
#         'population': item['population']})
#     conn.commit()
#     state_counter += 1


# Filling data table

# for item in api:
#     if item['date'] >= 20200326:
#         c.execute("SELECT date_id FROM date WHERE id = :id",
#                   {'id': item['date']})
#         date_id = c.fetchall()[0][0]
#         conn.commit()
#         c.execute("SELECT id FROM state WHERE abbreviation = :abbreviation",
#                   {'abbreviation': item['state']})
#         state_id = c.fetchall()[0][0]
#         conn.commit()
#         c.execute("INSERT INTO data VALUES (:id, :positive, :negative, :hospitalized, :death, :recovered, :pending, :state_id)",
#                   {'id': date_id,
#                    'positive': item['positive'],
#                    'negative': item['negative'],
#                    'hospitalized': item['hospitalized'],
#                    'death': item['death'],
#                    'recovered': item['recovered'],
#                    'pending': item['pending'],
#                    'state_id': state_id})
#         conn.commit()


# To reset table

# with conn:
#     c.execute("DROP TABLE state")
# with conn:
#     c.execute("""CREATE TABLE state (
#             id integer,
#             name text,
#             abbreviation text,
#             population integer
#         )""")


# with conn:
#     c.execute("SELECT date_id FROM date WHERE id = :id",
#               {'id': api[0]['date']})
#     print(c.fetchall()[0][0])


# with conn:
#     c.execute("SELECT id FROM state WHERE abbreviation = :abbreviation",
#               {'abbreviation': api[1]['state']})
#     print(c.fetchall()[0][0])


# used to write to a file (just so i could look at the data indented)

# f = open("historicalvalues.json", "w")
# f.write(json.dumps(api, indent=4))
# f.close()

# Close connection

conn.close()
