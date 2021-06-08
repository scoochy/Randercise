import threading

import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import sqlite3
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.properties import ListProperty

con = sqlite3.connect('exercises.db')

cur = con.cursor()

#cur.execute('''CREATE TABLE exercises (name text, difficulty text, muscles text)''')

#cur.execute("INSERT INTO exercises ('name', 'difficulty', 'muscles')  VALUES "
#            "('Push Up', 'Easy', 'Upper'),"
#            "('Yoga Push Up', 'Easy', 'Upper'),"
#            "('Downward Facing Dog Hold', 'Easy', 'Upper'),"
#            "('Sit Up', 'Easy', 'Core'),"
#            "('Mountain Climber', 'Easy', 'Core'),"
#            "('Leg Raises', 'Easy', 'Core'),"
#            "('Squat', 'Easy', 'Lower'),"
#            "('Lunges', 'Easy', 'Lower'),"
#            "('Hip Bridges', 'Easy', 'Lower'),"
#            "('Diamond Push Up', 'Medium', 'Upper'),"
#            "('Burpee Push Up', 'Medium', 'Upper'),"
#            "('Downward Facing Dog Push Up', 'Medium', 'Upper'),"
#            "('Crunches', 'Medium', 'Core'),"
#            "('Planck', 'Medium', 'Core'),"
#            "('Leg Raise Alternations', 'Medium', 'Core'),"
#            "('Single Leg Forward Squat', 'Medium', 'Lower'),"
#            "('Clockwork Lunges', 'Medium', 'Lower'),"
#            "('Burpees', 'Medium', 'Lower'),"
#            "('Pull Ups', 'Hard', 'Upper'),"
#            "('Handstand Shoulder Press', 'Hard', 'Upper'),"
#            "('Single Hand Push Ups', 'Hard', 'Upper'),"
#            "('Bicycle Crunches', 'Hard', 'Core'),"
#            "('Hanging Knee Raises', 'Hard', 'Core'),"
#            "('Hanging Leg Raises', 'Hard','Core'),"
#            "('Pistol Squats', 'Hard', 'Lower'),"
#            "('Alternating Jump Squats', 'Hard', 'Lower'),"
#            "('Hip Rotations', 'Hard', 'Lower')")


con.commit()


class MainWindow(Screen):
    exercises = []
    exercise_names = []


    def level(self, difficulty):
        self.difficulty = difficulty
        cur.execute("SELECT* FROM exercises WHERE difficulty = ?", (self.difficulty,))
        MainWindow.exercises = cur.fetchall()
        for row in MainWindow.exercises:
            MainWindow.exercise_names.append(row[0])







class SecondWindow(Screen):
    exercise_list = []
    exercise_list = MainWindow.exercise_names
    list_length = 0


    def my_callback(dt):
        print(SecondWindow.exercise_list), dt
        if len(SecondWindow.exercise_list) > 0:
            SecondWindow.list_length += 1
            print(SecondWindow.exercise_list[1])
            return False

    event = Clock.schedule_interval(my_callback, 1)


class ThirdWindow(Screen):
    pass

class FourthWindow(Screen):
    pass

class FifthWindow(Screen):
    pass

class WindowManager(ScreenManager):
    pass

kv = Builder.load_file("my.kv")

class MyMainApp(App):
    def build(self):
        return kv

if __name__ == "__main__":
    MyMainApp().run()