from db import get_db
import questionary as q
import sys


def analyze(tracker_name):
    choice = q.select("What would you like to do?",
                      choices=["View habits by frequency",
                               "View the longest streak",
                               "View the longest streak by frequency",
                               "Quit"]).ask()
    if choice == "View habits by frequency":
        view_habits_by_frequency(tracker_name)
        analyze(tracker_name)

    elif choice == "View the longest streak":
        view_the_longest_streak(tracker_name)
        analyze(tracker_name)

    elif choice == "View the longest streak by frequency":
        view_the_longest_streak_by_frequency(tracker_name)
        analyze(tracker_name)

    elif choice == "Quit":
        sys.exit()


def view_habits_by_frequency(tracker_name):
    choice = q.select('What frequency would you like to view?', choices=['daily', 'weekly']).ask()
    if choice == 'daily':
        frequency = 1
    elif choice == 'weekly':
        frequency = 7
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM habit WHERE tracker = ? AND frequency = ?', (tracker_name, frequency))
    habits = cur.fetchall()
    if len(habits) == 0:
        print(f'You have no habits with frequency {frequency}')
    else:
        print(f'\nYour habits with frequency {frequency}:\n')
        for habit in habits:
            print(f'{habit[0]} - {habit[3]} - {habit[6]}')


def view_the_longest_streak(tracker_name):
    pass


def view_the_longest_streak_by_frequency(tracker_name):
    pass
