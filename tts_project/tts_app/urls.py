from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from .secondviews import TextToSpeechView
from .views import TTSApiView, pause_mp3, play_mp3

urlpatterns = [
    path('api/tts/', TTSApiView.as_view(), name='tts_api'),
    path('playpause/', views.TTSApiView.as_view(), name='play_pause_api'),
    path('text-to-speech/', TextToSpeechView.as_view(), name='text-to-speech'),
    path('pause_speech/', views.pause_speech_view, name='pause_speech'),
    path('api/pause/', pause_mp3, name='pause-mp3'),
    path('api/play/<str:mp3_id>/', play_mp3, name='play-mp3'),

]


# from .views import TextToSpeechPlay, TextToSpeechPause, TextToSpeechCreate
#
# urlpatterns = [
#     path('api/tts/play/<int:tts_id>/', TextToSpeechPlay.as_view(), name='tts-play'),
#     path('api/tts/create/', TextToSpeechCreate.as_view(), name='tts-play'),
#
#     path('api/tts/pause/<int:tts_id>/', TextToSpeechPause.as_view(), name='tts-pause'),
# ]