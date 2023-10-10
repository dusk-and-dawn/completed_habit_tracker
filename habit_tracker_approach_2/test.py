from habits import Habit
from db import get_db, add_habit, increment_habit
import os
import pytest

class TestHabit: 

    def setup_method(self):
        self.db = get_db('test.db')

        add_habit(self.db, 'test_legend says this is a test_habit','test_Jo this be a fake habit', 'test_daily')
        increment_habit(self.db, 'test_legend says this is a test_habit', '2023-01-13')
        increment_habit(self.db, 'test_legend says this is a test_habit', '2023-01-14')

        increment_habit(self.db, 'test_legend says this is a test_habit', '2023-01-15')
        increment_habit(self.db, 'test_legend says this is a test_habit', '2023-01-16')

    def test_habit(self):
        habit = Habit('test_habit_da_legend', 'test_description_of_a_legend', 'test_period')

        habit.increment()
        habit.reset()
        habit.increment()

    def teardown_method(self):
        os.remove('test.db')