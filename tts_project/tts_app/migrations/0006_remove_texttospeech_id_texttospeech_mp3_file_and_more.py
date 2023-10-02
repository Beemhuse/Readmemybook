# Generated by Django 4.2.3 on 2023-09-07 13:07

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('tts_app', '0005_texttospeech_pdf_file_alter_texttospeech_text'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='texttospeech',
            name='id',
        ),
        migrations.AddField(
            model_name='texttospeech',
            name='mp3_file',
            field=models.FileField(blank=True, upload_to='mp3_files/'),
        ),
        migrations.AddField(
            model_name='texttospeech',
            name='mp3_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]