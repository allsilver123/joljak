# mysite/routing.py
from django.urls import path
from .consumers import VideoStreamConsumer

websocket_urlpatterns = [
    path('ws/video-stream2/', VideoStreamConsumer.as_asgi()),
]
