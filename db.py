import sqlite3
from datetime import datetime as dt
from datetime import timedelta as td

import questionary as q


def get_db(test=False):
    if test:
        conn = sqlite3.connect('test_database.db')
        return conn
    conn = sqlite3.connect('database.db')
    return conn


def create_tables():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS tracker (name TEXT PRIMARY KEY NOT NULL)')
    cur.execute('CREATE TABLE IF NOT EXISTS habit (name TEXT PRIMARY KEY NOT NULL, '
                'description TEXT NOT NULL, '
                'frequency_int INTEGER NOT NULL,'
                'frequency TEXT NOT NULL,'
                'last_completed_at TEXT,'
                'current_streak INTEGER NOT NULL DEFAULT 0,'
                'current_status TEXT NOT NULL DEFAULT "TO BE DONE",'
                ' tracker TEXT NOT NULL,'
                ' FOREIGN KEY(tracker) REFERENCES tracker(name))')
    conn.commit()


def view_habits(tracker_name):
    conn = get_db()
    cur = conn.cursor()
    update_habits_status(tracker_name)
    cur.execute('SELECT * FROM habit WHERE tracker = ?', (tracker_name,))
    habits = cur.fetchall()
    print('Here are your habits:')
    for habit in habits:
        print(habit)


def update_habits_status(tracker_name):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM habit WHERE tracker = ? AND current_status = "DONE"', (tracker_name,))
    habits = cur.fetchall()
    for habit in habits:
        if dt.today() - dt.strptime(habit[4], '%Y-%m-%d') > td(days=habit[2]):
            cur.execute('UPDATE habit SET current_status = ? WHERE tracker = ? AND name = ?',
                        ("TO BE DONE", tracker_name, habit[0]))
            conn.commit()
