from django.contrib import admin
from .models import Video, Subtitles

# Register your models here.
@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'upload_time')
    search_fields = ('title', 'description')

@admin.register(Subtitles)
class SubtitlesAdmin(admin.ModelAdmin):
    list_display = ('video', 'text')
    search_fields = ('video__title', 'text')