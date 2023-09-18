import questionary as q
from db import get_db

class Habit:
    def __init__(self, name, description, frequency, tracker):
        self.name = name
        self.description = description
        self.frequency = frequency
        self.tracker = tracker

    def __str__(self):
        return f'{self.name} - {self.frequency}'

def create_habit(tracker_name):
    name = q.text("What is the name of your Habit?").ask()
    description = q.text("What is the description of your Habit?").ask()
    choice = q.choice("What is the frequency of your Habit?", choices=['daily', 'weekly']).ask()
    if choice == 'daily':
        frequency = 1
    elif choice == 'weekly':
        frequency = 7
    habit = Habit(name, description, frequency, tracker_name)
    conn = get_db()
    cur = conn.cursor()
    cur.execute('INSERT INTO habit VALUES (?, ?, ?, ?)', (habit.name, habit.description, habit.frequency, habit.tracker))
    conn.commit()
    print(f'Created Habit {habit.name}')