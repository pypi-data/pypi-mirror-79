import pyttsx3

class Main:

    def __init__(self):

        self.eng = pyttsx3.init()
    def say_fraze(self, fraze):
        self.eng.say(fraze)
        self.eng.runAndWait()