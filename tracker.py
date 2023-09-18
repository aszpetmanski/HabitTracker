from db import get_db, create_tables
import questionary as q

class Tracker:
    def __init__(self, name):
        self.name = name

def create_tracker():
    name = q.text("What is the name of your Tracker?").ask()
    tracker = Tracker(name)
    create_tables()
    conn = get_db()
    cur = conn.cursor()
    cur.execute('INSERT INTO tracker VALUES (?)', (tracker.name,))
    conn.commit()
    print(f'Created Tracker {tracker.name}')
