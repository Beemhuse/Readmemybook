import threading

from rest_framework.views import APIView
from rest_framework.response import Response
import pyttsx3
import io
from pydub import AudioSegment

from .tts_app import text_to_speech

engine = pyttsx3.init()

class TextToSpeechView(APIView):
    def post(self, request, format=None):
        text = request.data.get('text')  # Get the text from the request data

        if text:
            mp3_data = text_to_speech(text)
            if mp3_data:
                return Response({'mp3_data': mp3_data}, status=200)
            else:
                return Response({'error': 'Error occurred during text-to-speech.'}, status=500)
        else:
            return Response({'error': 'No text provided.'}, status=400)

def text_to_speech(text):
    try:
        def speech_thread():
            nonlocal text
            engine.say(text)
            engine.runAndWait()

        # Start speech synthesis in a separate thread
        speech_thread = threading.Thread(target=speech_thread)
        speech_thread.start()

        speech_thread.join()

        temp_output_file = "output.wav"
        engine.save_to_file(text, temp_output_file)
        engine.runAndWait()


        audio = AudioSegment.from_wav(temp_output_file)

        mp3_buffer = io.BytesIO()
        audio.export(mp3_buffer, format='mp3')

        import os
        os.remove(temp_output_file)

        return mp3_buffer.getvalue()
    except Exception as e:
        print("Error during text-to-speech:", e)
        return None
