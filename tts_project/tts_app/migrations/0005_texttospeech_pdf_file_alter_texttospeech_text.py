# Generated by Django 4.2.3 on 2023-09-02 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tts_app', '0004_texttospeech_delete_convertedaudio'),
    ]

    operations = [
        migrations.AddField(
            model_name='texttospeech',
            name='pdf_file',
            field=models.FileField(blank=True, null=True, upload_to='pdf_files/'),
        ),
        migrations.AlterField(
            model_name='texttospeech',
            name='text',
            field=models.TextField(blank=True, null=True),
        ),
    ]
