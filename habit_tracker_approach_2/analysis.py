from db import get_habit_data
import calendar, pdb, datetime

def count_everything(db, habit):
    data = get_habit_data(db, habit)
    return len(data)

def count_dates(db, name):
    cur = db.cursor()
    cur.execute('SELECT date FROM tracker WHERE habitName=?', (name,))
    num_of_ind_dates = []
    all_dates = cur.fetchall()
    print(f'this is the all_dates content: {all_dates}')
    for i in all_dates:
        num_of_ind_dates.append(i)
    if len(num_of_ind_dates) == 1:
        pass 
    else:
        rem_duplicates = set(num_of_ind_dates)
        print(rem_duplicates)
        num_of_ind_dates = list(rem_duplicates)
    for i in num_of_ind_dates:
        if i == (None,):
            num_of_ind_dates.remove(i)
    try: 
        if num_of_ind_dates[0] == (None,) and num_of_ind_dates[-1] == (None,):
            return 0
    except IndexError:
        return 0
    return len(num_of_ind_dates)

def print_database_contents(db):
    cur = db.cursor()

    # Retrieve and print data from the habit table
    cur.execute("SELECT * FROM habit")
    habits = cur.fetchall()
    print("Habit Table Contents:")
    for habit in habits:
        print("Name:", habit[0])
        print("Description:", habit[1])
        print("Period:", habit[2])
        print()

    # Retrieve and print data from the tracker table
    cur.execute("SELECT * FROM tracker")
    tracker_data = cur.fetchall()
    print("Tracker Table Contents:")
    for data in tracker_data:
        print("Date:", data[0])
        print("Habit Name:", data[1])
        print()

    #db.close()  # Close the database connection

def streak_analysis(db):
    cal_year = calendar.calendar(2023)
    #print(cal_year)
    cur = db.cursor()
    cur.execute('SELECT * FROM tracker')
    tracker_data = cur.fetchall()
    #print(tracker_data)
    potential_streak_candidates = []
    dict_of_pot_streaks = {}
    for i in tracker_data: 
        if i[0] != None:
            potential_streak_candidates.append(i)
            #print(f'this is a non None type data element which we append to potential streak candidates: {i}')
    #print(potential_streak_candidates)
    rem_duplicates = list(set(potential_streak_candidates))
    potential_streak_candidates = sorted(rem_duplicates)
    #print(f'this is the psc list after duplicates are removed and the list is sorted: {potential_streak_candidates}')
    #pdb.set_trace()
    #counter = 1
    # for j in potential_streak_candidates:
    #     try:
    #         if j[1] == potential_streak_candidates[counter][1]:
    #             dict_of_pot_streaks[j[1]] = j[0], potential_streak_candidates[counter][0]
    #             print(f'these elements were just added as values to the dictionary: {j[0], potential_streak_candidates[counter][0]}')
    #         counter+=1
    #     except IndexError:
    #         print('index error encountered')
    #         pass
    
    # for i in range(len(potential_streak_candidates) - 1):
    #     print(f'value 1 being compared: {potential_streak_candidates[i][1]}')
    #     print(f'value 2 being compared: {potential_streak_candidates[i + 1][1]}')
    #     if potential_streak_candidates[i][1] == potential_streak_candidates[i + 1][1]:
    #         dict_of_pot_streaks[potential_streak_candidates[i][1]] = potential_streak_candidates[i][0], potential_streak_candidates[i + 1][0]

    # in this loop I build out my streak candidate dictionary so that I have habits as keys and all dates on which the habit was recorded as values 
    for i in potential_streak_candidates:
        temp_psc = potential_streak_candidates[:] # slicing here so as to not reference the original list 
        temp_psc.remove(i)
        temp_psc_habits = [j[1] for j in temp_psc] # this is probably super inefficient maybe use a different method later
        
        if i[1] in temp_psc_habits and i[1] not in dict_of_pot_streaks.keys(): # assigning the key the first time a habit shows up in the loop
            dict_of_pot_streaks[i[1]] = [i[0]]

        elif i[1] in temp_psc_habits and i[1] in dict_of_pot_streaks.keys(): # appending to the values for habits which are already keys in the dictionary
            dict_of_pot_streaks[i[1]].append(i[0])

    #print(f'these are potential streak candidates: {potential_streak_candidates}')
    #print(f'this is the dict of potential streaks: {dict_of_pot_streaks}')

    real_streaks = {}
    for key, values in dict_of_pot_streaks.items():
        #print(entry)
        first_date = datetime.datetime.strptime(values[0], '%Y-%m-%d') # transforms my string dates into datetime objects 
        last_date = datetime.datetime.strptime(values[-1], '%Y-%m-%d') 
        #print(type(first_date), first_date)
        
        len_habit_dates = len(values)
        len_real_dates = 0

        while first_date <= last_date:
            len_real_dates += 1
            first_date += datetime.timedelta(days=1)

        if len_habit_dates == len_real_dates:
            real_streaks[key] = values
        
    print(f'these are your streaks: {real_streaks}')
    longest_streak_info = {'habit':0, 'start_date':0, 'end_date':0, 'length':0}
    for key, values in real_streaks.items():
        if len(values) > longest_streak_info['length']:
            longest_streak_info['habit'] = key
            longest_streak_info['start_date'] = values[0]
            longest_streak_info['end_date'] = values[-1]
            longest_streak_info['length'] = len(values)

    print('congratulations, your longest streak is for\"',longest_streak_info['habit'], '\" which was first recorded on ',longest_streak_info['start_date'], '\n and lasted all the way to ',longest_streak_info['end_date'], 'for a total of ',longest_streak_info['length'], 'days. \n Amazing work!')
