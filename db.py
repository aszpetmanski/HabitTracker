import sqlite3
from datetime import datetime as dt
from datetime import timedelta as td


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
    cur.execute('CREATE TABLE IF NOT EXISTS habit (name TEXT NOT NULL, '
                'description TEXT NOT NULL, '
                'frequency_int INTEGER NOT NULL,'
                'frequency TEXT NOT NULL,'
                'last_completed_at TEXT,'
                'current_streak INTEGER NOT NULL DEFAULT 0,'
                'current_status TEXT NOT NULL DEFAULT "TO BE DONE",'
                ' tracker TEXT NOT NULL,'
                'PRIMARY KEY(name, tracker),'
                ' FOREIGN KEY(tracker) REFERENCES tracker(name) ON DELETE CASCADE)')
    cur.execute('CREATE TABLE IF NOT EXISTS habit_completed_at '
                '(habit_name TEXT NOT NULL,'
                'completed_at TEXT NOT NULL,'
                'tracker TEXT NOT NULL,'
                'PRIMARY KEY(habit_name, completed_at),'
                'FOREIGN KEY(habit_name, tracker) REFERENCES habit(name, tracker) ON DELETE CASCADE)')
    conn.commit()


def get_all_habits(tracker_name):
    conn = get_db()
    cur = conn.cursor()
    update_habits_status(tracker_name)
    cur.execute('SELECT * FROM habit WHERE tracker = ?', (tracker_name,))
    habits = cur.fetchall()
    return [habit for habit in habits]

def get_all_daily_habits(tracker_name):
    conn = get_db()
    cur = conn.cursor()
    update_habits_status(tracker_name)
    cur.execute('SELECT * FROM habit WHERE tracker = ? AND frequency_int = 1', (tracker_name,))
    habits = cur.fetchall()
    return [habit for habit in habits]


def view_habits(tracker_name):
    all_habits = get_all_habits(tracker_name)
    if len(all_habits) == 0:
        print('You have no habits yet')
    else:
        print('\nYour habits:\n')
        for habit in all_habits:
            print(f'{habit[0]} - {habit[1]} - {habit[3]} - {habit[6]}')
        print('\n')


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
