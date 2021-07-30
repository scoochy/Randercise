import os
os.environ['KIVY_VIDEO'] = 'ffpyplayer'
import kivy
kivy.require('1.9.0')
import random
import sqlite3

from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.accordion import Accordion, AccordionItem
from kivy.uix.screenmanager import ScreenManager, Screen

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
        if len(MainWindow.exercise_names) > 0:
            return False

    event = Clock.schedule_interval(my_callback, 1)


class ThirdWindow(Screen):
    setnumber = 1
    onpause = 3
    runningclock = 0

    def on_enter(self, *args):
        self.ids.timer.text = str(self.onpause)
        self.function_interval = Clock.schedule_interval(self.first_countdown, 1)
        self.ids.exercise.text = MainWindow.exercise_names[(self.setnumber - 1)]
        self.ids.next.text = MainWindow.exercise_names[(self.setnumber)]

    def first_countdown(self, *args):
        self.onpause -= 1
        self.ids.timer.text = str(self.onpause)
        if self.ids.timer.text == "0":
            Clock.unschedule(self.function_interval)
            Clock.unschedule(self.first_countdown)
            self.runningclock += 1
            self.onpause = 3
            self.event = Clock.schedule_interval(self.countdown, 1)



    def change_set(self, *args):
        if self.setnumber == len(MainWindow.exercise_names):
            self.ids.next.text = "You're almost there!"
            self.ids.set.text = str(self.setnumber)
            return False
        else:
            self.ids.next.text = MainWindow.exercise_names[self.setnumber]
            self.ids.set.text = str(self.setnumber)
            self.ids.exercise.text = MainWindow.exercise_names[(self.setnumber - 1)]

    def countdown(self, *args):
        self.ids.timer.text = str(self.onpause)
        self.onpause -= 1
        if self.ids.timer.text == "0":
            self.onpause = 3
            self.setnumber += 1
            if self.setnumber > len(MainWindow.exercise_names):
                self.change_screen()
            else:
                self.change_set()

    def pause_play(self):
        if self.runningclock == 1:
            self.ids.pause.text = "Play"
            Clock.unschedule(self.event)
            self.runningclock -= 1
        else:
            self.runningclock += 1
            self.ids.pause.text = "Pause ||"
            Clock.schedule_once(self.event)

    def change_screen(self):
        if self.manager.current == 'timer':
            self.manager.current = 'gif'
        else:
            self.manager.current = 'timer'

class FourthWindow(Screen):
    def on_enter(self, *args):
        Clock.schedule_once(self.change_screen, 5)

    def change_screen(self):
        if self.manager.current == 'gif':
            self.manager.current = 'cooldown'
        else:
            self.manager.current = 'gif'

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




if __name__ == "__main__":
    MyMainApp().run()