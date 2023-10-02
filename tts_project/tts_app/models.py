# tts_app/models.py

from django.db import models

# class MP3File(models.Model):
#     name = models.CharField(max_length=255, default="audio")
#     content = models.FileField(upload_to='mp3_files/')
#
#     def __str__(self):
#         return self.name
class TextToSpeech(models.Model):
        text = models.TextField(null=True, blank=True)
        pdf_file = models.FileField(upload_to='pdf_files/', null=True, blank=True)
        is_playing = models.BooleanField(default=False)

