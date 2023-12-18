from django.db import models
import uuid

# Create your models here.
def generate_video_filename(instance, filename):
    return f'video_{instance.uuid}.mp4'

class Video(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    upload_time = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='videos/')

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Customize the filename before saving
        self.file.name = generate_video_filename(self, self.file.name)
        super().save(*args, **kwargs)

class Subtitles(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    start_time = models.CharField(max_length=50, null=True)
    end_time = models.CharField(max_length=50, null=True)
    text = models.TextField()

    def __str__(self):
        return f"{self.video.title}"