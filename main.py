import sys
import questionary as q
from tracker import create_tracker
from habit import create_habit, delete_habit, mark_habit_as_done
from db import view_habits, get_db, create_tables, get_all_habits
from analyze import view_habits_by_frequency, view_the_longest_streak, view_the_longest_streak_by_frequency, view_my_daily_habit_tendency


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
            choices = [habit[0] for habit in get_all_habits(tracker_name) if habit[6] == 'TO BE DONE']
            choices.append('Back')
            habit_name = q.select('What is the name of the habit you would like to mark as completed?', choices=choices).ask()
            if habit_name == 'Back':
                view_habits(tracker_name)
            else:
                mark_habit_as_done(tracker_name, habit_name)
                view_habits(tracker_name)
        elif choice == 'Delete Habit':
            choices = [habit[0] for habit in get_all_habits(tracker_name)]
            choices.append('Back')
            habit_name = q.select('What is the name of the habit you would like to delete?', choices=choices).ask()
            if habit_name == 'Back':
                view_habits(tracker_name)
            else:
                delete_habit(tracker_name, habit_name)
                view_habits(tracker_name)
        tracker_menu(tracker_name)

    elif choice == "Analyze":
        analyze(tracker_name)
        tracker_menu(tracker_name)

    elif choice == "Quit":
        sys.exit()

def analyze(tracker_name):
    choice = q.select("What would you like to do?",
                      choices=["View habits by frequency",
                               "View the longest streak",
                               "View the longest streak by frequency",
                               "View my daily habit tendency",
                               "Back"]).ask()
    if choice == "View habits by frequency":
        view_habits_by_frequency(tracker_name)
        analyze(tracker_name)

    elif choice == "View the longest streak":
        view_the_longest_streak(tracker_name)
        analyze(tracker_name)

    elif choice == "View the longest streak by frequency":
        view_the_longest_streak_by_frequency(tracker_name)
        analyze(tracker_name)

    elif choice == "View my daily habit tendency":
        view_my_daily_habit_tendency(tracker_name)
        analyze(tracker_name)

    elif choice == "Back":
        tracker_menu(tracker_name)



if __name__ == '__main__':
    cli()
