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
from kivy.uix.image import Image
from kivy.uix.video import Video
from kivy.uix.label import Label


con = sqlite3.connect('exercises.db')

cur = con.cursor()

# cur.execute('''CREATE TABLE exercises (name text, difficulty text, muscles text)''')

# cur.execute("INSERT INTO exercises ('name', 'difficulty', 'muscles')  VALUES "
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
    exercise_advice = []
    exercise_tips = []
    random_exercises = []
    difficulty = 0
    number = 0

    def level(self, difficulty, number):
        MainWindow.difficulty = difficulty
        MainWindow.num_to_select = number
        if MainWindow.difficulty == "Easy":
            cur.execute("SELECT* FROM exercises WHERE difficulty = ?", (MainWindow.difficulty,))
            MainWindow.exercises = cur.fetchall()
            MainWindow.random_exercises = random.sample(MainWindow.exercises, self.num_to_select)
            for row in MainWindow.random_exercises:
                MainWindow.exercise_names.append(row[0])
                MainWindow.exercise_advice.append(row[3])
                MainWindow.exercise_tips.append(row[4])

        elif MainWindow.difficulty == "Medium":
            cur.execute("SELECT* FROM exercises WHERE difficulty = 'Easy' OR difficulty = ?", (MainWindow.difficulty,))
            MainWindow.exercises = cur.fetchall()
            MainWindow.random_exercises = random.sample(MainWindow.exercises, self.num_to_select)
            for row in MainWindow.random_exercises:
                MainWindow.exercise_names.append(row[0])
                MainWindow.exercise_advice.append(row[3])
                MainWindow.exercise_tips.append(row[4])

        elif MainWindow.difficulty == "Hard":
            cur.execute("SELECT* FROM exercises")
            MainWindow.exercises = cur.fetchall()
            MainWindow.random_exercises = random.sample(MainWindow.exercises, self.num_to_select)
            for row in MainWindow.random_exercises:
                MainWindow.exercise_names.append(row[0])
                MainWindow.exercise_advice.append(row[3])
                MainWindow.exercise_tips.append(row[4])

class Exercises(Accordion):

    def exercise_list(self):
        root = Accordion(orientation='vertical')

        for x in range(len(MainWindow.exercise_names)):
            item = AccordionItem(title='{}'.format(MainWindow.exercise_names[x]), size_hint_y = None, size_hint_x = 1)
            item.add_widget(Image(source = '{}'.format(MainWindow.exercise_tips[x])))
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
    setnumber = 0
    timer = 3
    runningclock = 1
    restingclock = -1
    worktime = 30
    resttime = 30

    def on_enter(self, *args):
        if MainWindow.difficulty == "Medium":
            self.resttime = 20
        if MainWindow.difficulty == "Hard":
            self.worktime = 45
            self.resttime = 15
        self.ids.timer.text = str(self.timer)
        self.function_interval = Clock.schedule_interval(self.first_countdown, 1)
        self.ids.exercise.text = MainWindow.exercise_names[(self.setnumber)]
        self.ids.next.text = MainWindow.exercise_names[self.setnumber + 1]
        self.ids.advice.source = MainWindow.exercise_tips[(self.setnumber)]

    def first_countdown(self, *args):
        self.timer -= 1
        self.ids.timer.text = str(self.timer)
        if self.ids.timer.text == "0":
            Clock.unschedule(self.function_interval)
            Clock.unschedule(self.first_countdown)
            self.setnumber += 1
            self.timer = self.worktime
            self.running = Clock.schedule_interval(self.countdown, 1)

    def change_set(self, *args):
        if self.setnumber == len(MainWindow.exercise_names):
            self.ids.next.text = "You're almost there!"
            self.ids.set.text = str(self.setnumber)
            self.ids.exercise.text = MainWindow.exercise_names[(self.setnumber - 1)]
            self.ids.advice.source = MainWindow.exercise_tips[(self.setnumber - 1)]
            return False
        else:
            self.ids.next.text = MainWindow.exercise_names[self.setnumber]
            self.ids.set.text = str(self.setnumber)
            self.ids.exercise.text = MainWindow.exercise_names[(self.setnumber - 1)]
            self.ids.advice.source = MainWindow.exercise_tips[(self.setnumber - 1)]
            print(self.setnumber)

    def countdown(self, *args):
        self.runningclock = 1
        self.restingclock = -1
        self.ids.timer.text = str(self.timer)
        self.timer -= 1
        if self.ids.timer.text == "0":
            self.timer = self.resttime
            self.ids.exercise.text = "Rest"
            self.restcountdown = Clock.schedule_interval(self.rest, 1)
            Clock.unschedule(self.running)

    def rest(self, *args):
        self.restingclock = 1
        self.runningclock = -1
        self.ids.timer.text = str(self.timer)
        self.timer -= 1
        if self.ids.timer.text == "0":
            Clock.unschedule(self.restcountdown)
            self.timer = self.worktime
            self.setnumber += 1
            if self.setnumber > len(MainWindow.exercise_names):
                self.change_screen()
                return False
            else:
                self.change_set()
                Clock.schedule_once(self.running)

    def pause_play(self):
        if self.setnumber == 0:
            if self.runningclock == 1:
                self.ids.pause.text = "Play"
                Clock.unschedule(self.function_interval)
                self.runningclock -= 1
            else:
                self.runningclock += 1
                self.ids.pause.text = "Pause ||"
                Clock.schedule_once(self.function_interval)
        else:

            if self.runningclock == 0:
                self.runningclock += 1
                self.ids.pause.text = "Pause ||"
                Clock.schedule_once(self.running)
                return False

            if self.runningclock == 1:
                self.ids.pause.text = "Play"
                Clock.unschedule(self.running)
                self.runningclock -= 1
                return False

            if self.restingclock == 0:
                self.ids.pause.text = "Pause ||"
                Clock.schedule_once(self.restcountdown)
                self.restingclock += 1
                return False

            if self.restingclock == 1:
                self.ids.pause.text = "Play"
                Clock.unschedule(self.restcountdown)
                self.restingclock -= 1
                return False


    def change_screen(self):
        if self.manager.current == 'timer':
            self.manager.current = 'gif'
        else:
            self.manager.current = 'timer'


class FourthWindow(Screen):
    def on_enter(self, *args):
        Clock.schedule_once(self.screen_change, 6)

    def screen_change(self, *args):
        self.manager.current = 'cooldown'


class FifthWindow(Screen):
    pass


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("my.kv")


class MyMainApp(App):
    sm = WindowManager()

    def build(self):
        return kv

if __name__ == "__main__":
    MyMainApp().run()
