from db import get_db
import questionary as q
import sys


def analyze(tracker_name):
    choice = q.select("What would you like to do?",
                      choices=["View habits by frequency",
                               "Quit"]).ask()
    if choice == "View habits by frequency":
        frequency = q.select("What frequency would you like to view?",
                             choices=["daily",
                                      "weekly"]).ask()
        if frequency == "daily":
            frequency = 1
        elif frequency == "weekly":
            frequency = 7

        view_habits_by_frequency(tracker_name, frequency)
        analyze(tracker_name)
    elif choice == "Quit":
        sys.exit()

def view_habits_by_frequency(tracker_name, frequency):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM habit WHERE tracker = ? AND frequency = ?', (tracker_name, frequency))
    habits = cur.fetchall()
    for habit in habits:
        print(habit)