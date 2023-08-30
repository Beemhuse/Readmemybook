# tts_app/tasks.py

import pyttsx3
from celery import Celery

app = Celery('speech', broker='redis://localhost:6379/0')

engine = pyttsx3.init()

class TextToSpeechTask:
    def __init__(self):
        self.paused = False
        self.text_content = ""

    @app.task
    def text_to_speech(self, text_content):
        self.text_content = text_content
        self.paused = False

        while not self.paused:
            engine.say(self.text_content)
            engine.runAndWait()

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

text_to_speech_task = TextToSpeechTask()
