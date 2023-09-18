import sqlite3

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
                'current_streak INTEGER NOT NULL, DEFAULT 0,'
                ' tracker TEXT NOT NULL,'
                ' FOREIGN KEY(tracker) REFERENCES tracker(name))')
    conn.commit()

def view_habits(tracker_name):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM habit WHERE tracker = ?', (tracker_name,))
    habits = cur.fetchall()
    print('Here are your habits:')
    for habit in habits:
        print(f'\nHabit: {habit[0]}, Description:  {habit[1]}, Frequency: {habit[3]}')

