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


def view_habits_by_frequency(tracker_name, frequency):
    pass


def view_the_longest_streak(tracker_name):
    pass


def view_the_longest_streak_by_frequency(tracker_name):
    pass
