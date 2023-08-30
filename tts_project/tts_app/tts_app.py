import io
import threading

import pyttsx3
from tkinter import Tk, filedialog
import fitz
from pydub import AudioSegment

from .player import Player  # Import your Player class here

player = Player()
engine = pyttsx3.init()
# Create a flag to control speech synthesis
is_speech_paused = False
speech_event = threading.Event()
def read_text_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            text_content = file.read()
            return text_content
    except IOError:
        print("Error: Unable to read the file.")
        return None

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

def text_to_speech(text_content):
    try:
        def speech_thread():
            global speech_event

            while not speech_event.is_set():
                engine.say(text_content)
                engine.runAndWait()

        # Start speech synthesis in a separate thread
        speech_thread = threading.Thread(target=speech_thread)
        speech_thread.start()


        # Start speech synthesis in a separate thread
        speech_thread = threading.Thread(target=speech_thread)
        speech_thread.start()

        # player.play()  # Start playing audio
        # Simulate the conversion process
        temp_output_file = "output.wav"
        engine.save_to_file(text_content, temp_output_file)
        engine.runAndWait()

        # Wait for the speech thread to complete
        speech_thread.join()
        player.pause()

        # Convert the WAV file to MP3 using pydub
        audio = AudioSegment.from_wav(temp_output_file)

        # Export the MP3 data as bytes
        mp3_buffer = io.BytesIO()
        audio.export(mp3_buffer, format='mp3')

        # Remove the temporary WAV file
        import os
        os.remove(temp_output_file)

        return mp3_buffer.getvalue()  # Return the binary data of the MP3 file
    except Exception as e:
        print("Error during text-to-speech:", e)
        return None
def pause_speech():
    """Pause speech synthesis."""
    speech_event.set()

def resume_speech():
    """Resume speech synthesis."""
    speech_event.clear()

# def text_to_speech(text_content):
#     try:
#         engine = pyttsx3.init()
#         engine.say(text_content)
#         engine.runAndWait()
#
#
#         temp_output_file = "output.wav"
#         engine.save_to_file(text_content, temp_output_file)
#         engine.runAndWait()
#
#         # Convert the WAV file to MP3 using pydub
#         audio = AudioSegment.from_wav(temp_output_file)
#
#         # Export the MP3 data as bytes
#         mp3_buffer = io.BytesIO()
#         audio.export(mp3_buffer, format='mp3')
#
#         # Remove the temporary WAV file
#         import os
#         os.remove(temp_output_file)
#
#         return mp3_buffer.getvalue()  # Return the binary data of the MP3 file
#     except Exception as e:
#         print("Error during text-to-speech:", e)
#         return None
def main():
    Tk().withdraw()  # Prevent the Tkinter window from appearing
    file_path = filedialog.askopenfilename(title="Select a file", filetypes=[("Text files", "*.txt"), ("PDF files", "*.pdf")])

    if file_path:
        if file_path.endswith('.txt'):
            text_content = read_text_from_file(file_path)
        elif file_path.endswith('.pdf'):
            text_content = read_pdf_content(file_path)
        else:
            print("Unsupported file format.")
            return
        if text_content:
            text_to_speech(text_content)
        else:
            print("No content in the file or an error occurred while reading.")
    else:
        print("No file selected.")

if __name__ == "__main__":
    main()



