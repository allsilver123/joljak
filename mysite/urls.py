# mysite/urls.py
from django.urls import path, include
from . import views
from django.contrib import admin
from .consumers import VideoStreamConsumer

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('common.urls')),
    path('main/', views.main_page,  name='main_page'),
    path('video-stream/', views.video_stream, name='video-stream'),
    path('upload/', views.upload,  name='upload'),
    path('start/', views.start,  name='start'), 
    path('main/msg-test/', views.msg_test,  name='msg-test'), 

    path('common/', include('common.urls')),
]
