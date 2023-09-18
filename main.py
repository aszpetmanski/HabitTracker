import sys
import questionary as q
from tracker import create_tracker
from habit import create_habit
from db import view_habits
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
        tracker_menu(tracker_name)

    elif choice == "Analyze":
        analyze(tracker_name)
        tracker_menu(tracker_name)

    elif choice == "Quit":
        sys.exit()


