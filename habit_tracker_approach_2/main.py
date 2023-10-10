from db import *
from habits import Habit
from analysis import *
import questionary

def cli():
    db = get_db() 
    questionary.confirm('Welcome to David\'s Habit Tracker, are you ready to proceed?').ask()
    stop = False

    while not stop:
        choice = questionary.select('How can I be helpful?', 
        choices=['create', 'record habit', 'analyze individual habit', 'analyze streaks', 'reset habit', 'show me all you\'ve got', 'exit']).ask()

        if choice == 'create':
            name = questionary.text('what new habit would you like to create?').ask()
            description = questionary.text('please do describe your new habit: ').ask()
            period = questionary.select('please choose between daily and weekly', ('daily', 'weekly')).ask()
            habit = Habit(name, description, period)
            habit.store(db)
        elif choice == 'record habit':
            list_for_picking = get_just_habits(db)
            dict_final_choices = {}
            for entry in list_for_picking:
                dict_final_choices[entry]=entry
            pick_habit = questionary.select('please do choose one of the following habits to record:', choices=dict_final_choices).ask()
            description2 = '\'sup this is filler text'
            period = 'more filler text'
            habit = Habit(pick_habit, description2, period)
            habit.increment(db)
            habit.add_event(db)
        elif choice == 'analyze individual habit': 
            list_for_picking = get_just_habits(db)
            dict_final_choices = {}
            for entry in list_for_picking:
                dict_final_choices[entry]=entry
            name = questionary.select('Select the name of the habit you want to analyze: ', choices=dict_final_choices).ask()
            count = count_dates(db, name)
            print(f'{name} has been recorded {count} times.')
        elif choice == 'show me all you\'ve got':
            print_database_contents(db)
            #get_just_habits(db)
        elif choice == 'reset habit':
            list_for_picking = get_just_habits(db)
            dict_final_choices = {}
            for entry in list_for_picking:
                dict_final_choices[entry]=entry
            chosen_habit = questionary.select('which habit would you like to reset:', choices=dict_final_choices).ask()
            description2 = '\'sup this is filler text'
            period = 'more filler text'
            habit = Habit(chosen_habit, description2, period)
            habit.reset(db)
        elif choice == 'analyze streaks':
            streak_analysis(db)
            #print('unfrotunately, this feature has not been implemented yet')
        else: 
            print('I really hope I did a good job, thank you for using my functionalities.')
            stop = True

if __name__ == '__main__':
    cli()




