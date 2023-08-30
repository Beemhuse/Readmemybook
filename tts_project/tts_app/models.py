# tts_app/models.py

from django.db import models

class MP3File(models.Model):
    name = models.CharField(max_length=255, default="audio")
    content = models.FileField(upload_to='mp3_files/')

    def __str__(self):
        return self.name
