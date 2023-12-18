from django.shortcuts import render, redirect
from .models import Video
from .forms import VideoForm 
from django.http import HttpResponse
from .utils import process_video
import boto3
from boto3.dynamodb.conditions import Key
from django.core.files.storage import FileSystemStorage

def upload_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.save()
            video_file = request.FILES['file']
            fs = FileSystemStorage()
            filename = fs.save(f'videos/video_{video.uuid}.mp4', video_file)
            process_video.delay(video.uuid)
            return redirect('upload_video')
    else:
        form = VideoForm()

    uploaded_videos = Video.objects.all()

    return render(request, 'upload_video.html', {'form': form, 'uploaded_videos': uploaded_videos})

def search_videos(request, video_id):
    keyword = request.GET.get('keyword')

    try:
        video = Video.objects.get(uuid=video_id)
    except Video.DoesNotExist:
        return HttpResponse("Video not found")

    # Connect to DynamoDB
    aws_access_key_id = '*****'
    aws_secret_access_key = '********'
    region_name = '******'
    dynamodb = boto3.resource('dynamodb', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region_name)
    table_name = 'subtitles'
    table = dynamodb.Table(table_name)

    response = table.query(
        KeyConditionExpression=Key('video_id').eq(str(video_id))
    )
    results = response.get('Items', [])
    if keyword:
        matching_subtitles = [subtitle for subtitle in results if keyword_in_subtitle(subtitle['content'], keyword)]
        context = {'results': matching_subtitles, 'keyword': keyword, 'url': video.file.url, "title": video.title}
    else:
        context = {'results': results, 'keyword': keyword, 'url': video.file.url, "title": video.title}
    return render(request, 'search_results.html', context)

def keyword_in_subtitle(subtitle, keyword):
    return keyword.lower() in subtitle.lower()
