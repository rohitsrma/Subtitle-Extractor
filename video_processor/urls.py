# video_processor/urls.py

from django.urls import path
from video_processor import views

urlpatterns = [
    path('upload/', views.upload_video, name='upload_video'),
    path('search_videos/<uuid:video_id>/', views.search_videos, name='search_videos'),
]
