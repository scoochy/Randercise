import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import sqlite3

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
con.close()

class MainWindow(Screen):
    pass

class SecondWindow(Screen):
    pass

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