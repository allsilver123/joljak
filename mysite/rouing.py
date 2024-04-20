# your_app/routing.py

from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/process_image/', consumers.ImageProcessConsumer.as_asgi()),
]
