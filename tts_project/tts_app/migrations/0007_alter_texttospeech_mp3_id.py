# Generated by Django 4.2.3 on 2023-09-07 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tts_app', '0006_remove_texttospeech_id_texttospeech_mp3_file_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='texttospeech',
            name='mp3_id',
            field=models.UUIDField(editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
