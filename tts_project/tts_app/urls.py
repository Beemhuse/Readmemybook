from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from .secondviews import TextToSpeechView
from .views import TTSApiView

urlpatterns = [
    path('api/tts/', TTSApiView.as_view(), name='tts_api'),
    path('playpause/', views.TTSApiView.as_view(), name='play_pause_api'),
    path('text-to-speech/', TextToSpeechView.as_view(), name='text-to-speech'),
    path('pause_speech/', views.pause_speech_view, name='pause_speech'),
    path('resume_speech/', views.resume_speech_view, name='resume_speech'),
    path('play-speech/', views.play_speech_view, name='play_speech'),
]