import questionary as q
from db import get_db
from timespan import TimeSpan
from tracker import Tracker

class Habit:
    def __init__(self, name: str, description: str, frequency: TimeSpan, tracker: Tracker):
        self.name = name
        self.description = description
        self.frequency = frequency
        self.tracker = tracker

    def __str__(self):
        return f'{self.name} - {self.frequency}'


def create_habit(tracker):
    name = q.text("What is the name of your Habit?").ask()
    description = q.text("What is the description of your Habit?").ask()
    choice = q.select("What is the frequency of your Habit?", choices=['daily', 'weekly']).ask()
    if choice == 'daily':
        frequency = TimeSpan(1)
    elif choice == 'weekly':
        frequency = TimeSpan(7)
    habit = Habit(name, description, frequency, tracker)
    conn = get_db()
    cur = conn.cursor()
    cur.execute('INSERT INTO habit VALUES (?, ?, ?, ?, ?)',
                (habit.name, habit.description, habit.frequency.span, str(habit.frequency), habit.tracker))
    conn.commit()
    print(f'Created Habit {habit.name}')

def delete_habit(tracker_name, habit_name):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('DELETE FROM habit WHERE tracker = ? AND name = ?', (tracker_name, habit_name))
    conn.commit()
    print(f'Deleted Habit {habit_name}')
