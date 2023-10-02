from rest_framework import serializers
from .models import TextToSpeech

class TextToSpeechSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextToSpeech
        fields = '__all__'
