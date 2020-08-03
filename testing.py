import sqlite3
from datetime import datetime, timedelta


def update_database():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()


def read_database_positive_today():
    print(datetime.now() + timedelta(hours=3))


read_database_positive_today()
