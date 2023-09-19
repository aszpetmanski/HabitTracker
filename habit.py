import questionary as q
from db import get_db, get_all_habits
from timespan import TimeSpan
from tracker import Tracker
from datetime import date as dt


class Habit:
    def __init__(self, name: str, description: str, frequency: TimeSpan, tracker: Tracker):
        self.name = name
        self.description = description
        self.frequency = frequency
        self.tracker = tracker

    def __str__(self):
        return f'{self.name} - {self.frequency}'


def create_habit(tracker):
    habit_names = [habit[0] for habit in get_all_habits(tracker)]
    name = q.text("What is the name of your Habit?",
                  validate=lambda text: True if text not in habit_names else
                  'Habit with this name already exsists').ask()
    description = q.text("What is the description of your Habit?").ask()
    choice = q.select("What is the frequency of your Habit?", choices=['daily', 'weekly']).ask()
    if choice == 'daily':
        frequency = TimeSpan(1)
    elif choice == 'weekly':
        frequency = TimeSpan(7)
    habit = Habit(name, description, frequency, tracker)
    conn = get_db()
    cur = conn.cursor()
    cur.execute('INSERT INTO habit VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                (habit.name, habit.description, habit.frequency.span, str(habit.frequency), None, 0, "TO BE DONE",
                 habit.tracker))
    conn.commit()
    print(f'Created Habit {habit.name}')


def delete_habit(tracker_name, habit_name):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('DELETE FROM habit WHERE tracker = ? AND name = ?', (tracker_name, habit_name))
    conn.commit()
    print(f'Deleted Habit {habit_name}')


def mark_habit_as_done(tracker_name, habit_name):
    conn = get_db()
    cur = conn.cursor()
    update_habit_streak(tracker_name, habit_name)
    cur.execute('UPDATE habit SET last_completed_at = ?, current_status = ? WHERE tracker = ? AND name = ?',
                (dt.today(), "DONE", tracker_name, habit_name))
    conn.commit()
    print(f'Marked Habit {habit_name} as done')


def update_habit_streak(tracker_name, habit_name):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM habit WHERE tracker = ? AND name = ?', (tracker_name, habit_name))
    habit = cur.fetchone()
    if habit[5] == 0:
        cur.execute('UPDATE habit SET current_streak = ? WHERE tracker = ? AND name = ?', (1, tracker_name, habit_name))
        conn.commit()
    elif habit[5] > 0:
        if dt.today() - habit[4] <= habit[2]:
            cur.execute('UPDATE habit SET current_streak = ? WHERE tracker = ? AND name = ?',
                        (habit[5] + 1, tracker_name, habit_name))
            conn.commit()
        elif dt.today() - habit[4] > habit[2]:
            cur.execute('UPDATE habit SET current_streak = ? WHERE tracker = ? AND name = ?',
                        (1, tracker_name, habit_name))
            conn.commit()
