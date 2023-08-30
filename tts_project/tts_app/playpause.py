# tts_api/playpause.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from tts_project.tts_app.player import Player


# from . import Player


# from .player import player

class TTSPlayView(APIView):
    def patch(self, request, *args, **kwargs):
        Player.play()
        return Response({'message': 'Playback resumed.'}, status=status.HTTP_200_OK)

class TTSPauseView(APIView):
    def patch(self, request, *args, **kwargs):
        Player.pause()
        return Response({'message': 'Playback paused.'}, status=status.HTTP_200_OK)
