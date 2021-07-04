import threading

import kivy
import time
import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import sqlite3
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.uix.accordion import Accordion, AccordionItem
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
    random_exercises = []




    def level(self, difficulty, number):
        self.difficulty = difficulty
        self.num_to_select = number
        cur.execute("SELECT* FROM exercises WHERE difficulty = ?", (self.difficulty,))
        MainWindow.exercises = cur.fetchall()
        MainWindow.random_exercises = random.sample(MainWindow.exercises, self.num_to_select)
        for row in MainWindow.random_exercises:
            MainWindow.exercise_names.append(row[0])


class Exercises(Accordion):
    def exercise_list(self):
        root = Accordion(orientation = 'vertical')

        for x in range (len(MainWindow.exercise_names)):
            item = AccordionItem(title = '{}'.format(MainWindow.exercise_names[x]))
            root.add_widget(item)
        return root


class SecondWindow(Screen):


    def on_enter(self, *args):
        if self.my_callback() == False:
            exerlist = Exercises.exercise_list(self)
            self.ids.grid.add_widget(exerlist)

    def my_callback(dt):
        print(MainWindow.exercise_names), dt
        if len(MainWindow.exercise_names) > 0:
            print(MainWindow.exercise_names[0])
            return False

    event = Clock.schedule_interval(my_callback, 1)


class ThirdWindow(Screen):
    play = 0


    def on_enter(self):
        self.function_interval = Clock.schedule_interval(self.countdown, 1)
        Clock.schedule_once(self.stop_timer, 3)
        self.ids.exercise.text = MainWindow.exercise_names[0]
        self.ids.next.text = MainWindow.exercise_names[1]



    def stop_timer(self, *args):
        self.function_interval.cancel()
        self.set_number()
        self.reset_timer()


    def countdown(self, *args):
        self.ids.timer.text = str(int(self.ids.timer.text) - 1)

    def set_number(self):
        Clock.schedule_interval(self.change_set, 30)


    def change_set(self, *args):
        self.ids.set.text = str(int(self.ids.set.text) + 1)
        self.ids.exercise.text = MainWindow.exercise_names[int(self.ids.set.text) - 1]
        if self.ids.set.text == str(len(MainWindow.exercise_names)):
            self.ids.next.text = "You're almost there!"
            return False
        else:
            self.ids.next.text = MainWindow.exercise_names[int(self.ids.set.text)]


    def reset_timer(self, *args):
        self.ids.timer.text = "30"
        Clock.schedule_interval(self.timer_loop, 30)
        Clock.schedule_interval(self.set_countdown, 1)


    def set_countdown(self, *args):
        if self.pause == False:
            self.ids.timer.text = str(int(self.ids.timer.text) - 1)
        else:
            Clock.unschedule(self.set_countdown)

    def timer_loop(self, *args):
        self.ids.timer.text = "30"

    def pause(self, *args):
        if self.play > 0:
            Clock.schedule_interval(self.set_countdown, 1)
            return False



class FourthWindow(Screen):
    pass

class FifthWindow(Screen):
    pass

class WindowManager(ScreenManager):
    pass

kv = Builder.load_file("my.kv")

class MyMainApp(App):
    sm = WindowManager()
    def build(self):
        return kv
        return sm
    def on_pause(self):
        return True



if __name__ == "__main__":
    MyMainApp().run()