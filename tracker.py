from db import get_db, create_tables
import questionary as q


class Tracker:
    """Tracker class"""
    def __init__(self, name):
        self.name = name


def create_tracker():
    """This function validates the tracker name and creates a new tracker in the database"""
    create_tables()
    conn = get_db()
    cur = conn.cursor()
    tracker_names = get_all_tracker_names(cur)
    name = q.text("What is the name of your Tracker?", validate=lambda text: True if text not in tracker_names
        else 'This tracker name is already taken').ask()
    tracker = Tracker(name)
    cur.execute('INSERT INTO tracker VALUES (?)', (tracker.name,))
    conn.commit()
    print(f'\nCreated Tracker {tracker.name}\n')


def get_all_tracker_names(cur):
    """This function returns a list of all tracker names"""
    cur.execute('SELECT name FROM tracker')
    tracker_names = cur.fetchall()
    return [tracker_name[0] for tracker_name in tracker_names]
