from db import get_db
import questionary as q
import sys
from datetime import date, timedelta
from db import get_all_habits, get_all_daily_habits


def view_habits_by_frequency(tracker_name):
    """View habits by frequency"""
    choice = q.select('What frequency would you like to view?', choices=['daily', 'weekly']).ask()
    if choice == 'daily':
        frequency = 1
    elif choice == 'weekly':
        frequency = 7
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM habit WHERE tracker = ? AND frequency_int = ?', (tracker_name, frequency))
    habits = cur.fetchall()
    if len(habits) == 0:
        print(f'You have no habits with that frequency yet.')
    else:
        print(f'\nYour habits with frequency {choice}:\n')
        for habit in habits:
            print(f'{habit[0]} - {habit[3]} - {habit[6]}')
    print('\n')


def view_the_longest_streak(tracker_name):
    """View the longest streak"""
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM habit WHERE tracker = ? ORDER BY current_streak DESC', (tracker_name,))
    habit = cur.fetchone()
    if habit[5] == 0:
        print('You have no habits yet')
    else:
        print(f'\nYour longest streak is {habit[5]} and is for your {habit[3]} habit {habit[0]}\n')


def view_the_longest_streak_by_frequency(tracker_name):
    """View the longest streak by frequency"""
    choice = q.select('What frequency would you like to view?', choices=['daily', 'weekly']).ask()
    if choice == 'daily':
        frequency = 1
    elif choice == 'weekly':
        frequency = 7
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM habit WHERE tracker = ? AND frequency_int = ? ORDER BY current_streak DESC',
                (tracker_name, frequency))
    habit = cur.fetchone()
    if habit[5] == 0:
        print(f'You have no completed habits with that frequency yet.')
    else:
        print(f'\nYour longest streak is {habit[5]} and is for your {habit[3]} habit {habit[0]}\n')
    print('\n')

def view_my_daily_habit_tendency(tracker_name):
    """View my daily habit tendency"""
    habit_name = q.select('What habit would you like to view?', choices=[habit[0] for habit in get_all_daily_habits(tracker_name)]).ask()
    last_28_days = sorted([str(date.today() - timedelta(days=i)) for i in range(28)])
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM habit_completed_at WHERE tracker = ? AND habit_name = ?', (tracker_name, habit_name))
    habits_completed_at = sorted([habit[1] for habit in cur.fetchall()])
    tendency_string = ''
    score = 0
    for day in last_28_days:
        if day in habits_completed_at:
            tendency_string += 'O '
            score += 1
        else:
            tendency_string += 'X '
    tendency_string += f'          OVERALL TENDENCY: {score}/28'
    print('\n' + tendency_string + '\n')
