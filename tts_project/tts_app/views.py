import base64
import uuid

import fitz
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
import io
import pyttsx3
import threading
from pydub import AudioSegment

from .player import Player
from .tasks import text_to_speech_task

engine = pyttsx3.init()
player = Player()

class TTSApiView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, format=None):
        if 'file' not in request.data:
            return Response({'error': 'No file part in the request.'}, status=400)

        uploaded_file = request.data['file']
        file_content = uploaded_file.read()

        if uploaded_file.name.endswith('.txt'):
            text_content = file_content.decode('utf-8')
        elif uploaded_file.name.endswith('.pdf'):
            text_content = read_pdf_content(file_content)
            if text_content is None:
                return Response({'error': 'Error: Unable to extract text from the PDF.'}, status=400)
        else:
            return Response({'error': 'Unsupported file format.'}, status=400)

        if text_content:
            mp3_data = text_to_speech(text_content)
            mp3_id = str(uuid.uuid4())
            print(mp3_id)

            if mp3_data:
                # Save the MP3 data in a global dictionary with the MP3 ID as the key
                mp3_storage[mp3_id] = mp3_data
                download_url = reverse('download-mp3', kwargs={'mp3_id': mp3_id})

                encoded_mp3_data = base64.b64encode(mp3_data).decode('utf-8')

                # Return the MP3 ID in the response
                return JsonResponse({'mp3_id': mp3_id, 'mp3_data': encoded_mp3_data}, status=201)
            else:
                return Response({'error': 'Error occurred during text-to-speech.'}, status=500)
        else:
            return Response({'error': 'No content in the file or an error occurred while reading.'}, status=400)

# Initialize a global dictionary to store MP3 data with their respective IDs
mp3_storage = {}


# Function to initiate play and pause functionality
def play_mp3(mp3_id):
    mp3_data = mp3_storage.get(mp3_id)
    if mp3_data:
        audio = AudioSegment.from_mp3(io.BytesIO(mp3_data))
        player.play(audio)
    else:
        return Response({'error': 'MP3 with the specified ID not found.'}, status=404)

def pause_mp3():
    player.pause()


    def patch(self, request, format=None):
        action = request.query_params.get('action')

        if action == 'play':
            play_and_speak()
            # player.play()
            return JsonResponse({'message': 'Playback resumed.'}, status=200)
        elif action == 'pause':
            player.pause()
            return JsonResponse({'message': 'Playback paused.'}, status=200)
        else:
            return JsonResponse({'error': 'Invalid action.'}, status=400)
def pause_speech_view(request):
    text_to_speech_task.pause()
    return JsonResponse({'message': 'Speech paused'})

def resume_speech_view(request):
    text_to_speech_task.resume()
    return JsonResponse({'message': 'Speech resumed'})
def read_pdf_content(file_content):
    try:
        text_content = ""
        pdf_file = io.BytesIO(file_content)
        pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")

        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            text_content += page.get_text()

        pdf_document.close()

        return text_content
    except Exception as e:
        print("Error while reading PDF:", e)
        return None
def play_speech_view(request):
    if not text_to_speech_task.text_content:
        # If text_content is empty, fetch the content to be played
        # You can fetch content from your source here
        text_to_speech_task.text_content = "Your text content goes here"

    text_to_speech_task.text_to_speech(text_to_speech_task.text_content)
    return JsonResponse({'message': 'Speech started'})
def text_to_speech(text_content):
    try:
        def speech_thread():
            nonlocal text_content
            engine.say(text_content)
            engine.runAndWait()

        # Start speech synthesis in a separate thread
        speech_thread = threading.Thread(target=speech_thread)
        speech_thread.start()

        player.play()
        temp_output_file = "output.wav"
        engine.save_to_file(text_content, temp_output_file)
        engine.runAndWait()

        speech_thread.join()
        player.pause()

        audio = AudioSegment.from_wav(temp_output_file)

        mp3_buffer = io.BytesIO()
        audio.export(mp3_buffer, format='mp3')

        import os
        os.remove(temp_output_file)

        return mp3_buffer.getvalue()
    except Exception as e:
        print("Error during text-to-speech:", e)
        return None

def play_and_speak():
    player.play()
    text_to_speech("Your text here")
    player.pause()

# # import base64
# #
# # from rest_framework import status
# # from rest_framework.views import APIView
# # from rest_framework.parsers import MultiPartParser
# # from rest_framework.response import Response
# # from django.http import HttpResponse, JsonResponse
# # import pyttsx3
# # from .player import Player  # Assuming you have a player module in your app
# # from .tts_app import read_text_from_file, read_pdf_content, text_to_speech
# # from .models import MP3File
# # # paused = False
# # engine = pyttsx3.init()
# # player = Player()  # Initialize the player
# #
# # class TTSApiView(APIView):
# #     parser_classes = [MultiPartParser]
# #
# #     def post(self, request, format=None):
# #         if 'file' not in request.data:
# #             return Response({'error': 'No file part in the request.'}, status=400)
# #
# #         uploaded_file = request.data['file']
# #         file_content = uploaded_file.read()
# #
# #         if uploaded_file.name.endswith('.txt'):
# #             text_content = file_content.decode('utf-8')
# #         elif uploaded_file.name.endswith('.pdf'):
# #             text_content = read_pdf_content(file_content)
# #             if text_content is None:
# #                 return Response({'error': 'Error: Unable to extract text from the PDF.'}, status=400)
# #         else:
# #             return Response({'error': 'Unsupported file format.'}, status=400)
# #
# #         if text_content:
# #             mp3_data = text_to_speech(text_content)
# #             if mp3_data:
# #                 encoded_mp3_data = base64.b64encode(mp3_data).decode('utf-8')
# #                 return JsonResponse({'mp3_data': encoded_mp3_data}, status=201)
# #             else:
# #                 return Response({'error': 'Error occurred during text-to-speech.'}, status=500)
# #         else:
# #             return Response({'error': 'No content in the file or an error occurred while reading.'}, status=400)
# #
# #     # def get(self, request, mp3_id=None, format=None):
# #     #     if mp3_id is not None:
# #     #         try:
# #     #             mp3_file = MP3File.objects.get(pk=mp3_id)
# #     #             return HttpResponse(mp3_file.content, content_type='audio/mpeg')
# #     #         except MP3File.DoesNotExist:
# #     #             return Response({'error': 'MP3 file not found.'}, status=404)
# #     #     else:
# #     #         return Response({'error': 'Invalid request.'}, status=400)
# #
# #     def patch(self, request, format=None):
# #
# #         action = request.query_params.get('action')
# #
# #         if action == 'play':
# #             player.play()  # Assuming your Player class has a play() method
# #             return Response({'message': 'Playback resumed.'}, status=200)
# #         elif action == 'pause':
# #             player.pause()  # Assuming your Player class has a pause() method
# #             return Response({'message': 'Playback paused.'}, status=200)
# #         else:
# #             return Response({'error': 'Invalid action.'}, status=400)
# #
# # class PlaybackStateView(APIView):
# #     def get(self, request, format=None):
# #         return Response({'playing': player.is_playing()}, status=status.HTTP_200_OK)
