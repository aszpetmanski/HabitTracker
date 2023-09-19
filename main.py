import sys
import questionary as q
from tracker import create_tracker
from habit import create_habit, delete_habit, mark_habit_as_done
from db import view_habits, get_db, create_tables
from analyze import analyze


def cli():
    while True:
        main_menu()


def main_menu():
    choice = q.select("What would you like to do?",
                      choices=["Log to your Tracker (use 'test' name for testing)",
                               "Create new Tracker",
                               "Quit"]).ask()

    if choice == "Log to your Tracker (use 'test' name for testing)":
        log_in()

    elif choice == "Create new Tracker":
        create_tracker()
        main_menu()

    elif choice == "Quit":
        sys.exit()


def log_in():
    tracker_name = q.text("What is the name of your Tracker?").ask()
    if tracker_name == 'test':
        conn = get_db(test=True)
        create_tables()
        tracker_menu(tracker_name)
    tracker_menu(tracker_name)


def tracker_menu(tracker_name):
    choice = q.select("What would you like to do?",
                      choices=["Create new Habit",
                               "View Habits",
                               "Analyze",
                               "Quit"]).ask()

    if choice == "Create new Habit":
        create_habit(tracker_name)
        tracker_menu(tracker_name)

    elif choice == "View Habits":
        view_habits(tracker_name)
        choice = q.select('OPTIONS', choices=['Create new Habit', 'Mark Habit as completed', 'Delete Habit', 'Go back']).ask()
        if choice == 'Create new Habit':
            create_habit(tracker_name)
            view_habits(tracker_name)

        elif choice == 'Mark Habit as completed':
            habit_name = q.text('What is the name of the habit you would like to mark as completed?').ask()
            mark_habit_as_done(tracker_name, habit_name)
            view_habits(tracker_name)
        elif choice == 'Delete Habit':
            habit_name = q.text('What is the name of the habit you would like to delete?').ask()
            delete_habit(tracker_name, habit_name)
            view_habits(tracker_name)
        tracker_menu(tracker_name)

    elif choice == "Analyze":
        analyze(tracker_name)
        tracker_menu(tracker_name)

    elif choice == "Quit":
        sys.exit()


if __name__ == '__main__':
    cli()
