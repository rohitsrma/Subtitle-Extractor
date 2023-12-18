import subprocess
import os
import logging
import boto3
from django.conf import settings
from .models import Video
from celery import shared_task

logger = logging.getLogger(__name__)

def parse_time_range(time_range):
    start, end = time_range.split(' --> ')
    return start, end

@shared_task
def process_video(video_id):
    try:
        video = Video.objects.get(uuid=video_id)
    except Video.DoesNotExist:
        logger.error(f"Video with ID {video_id} not found.")
        return "Video not found"

    input_path = os.path.join(settings.MEDIA_ROOT, "videos", f'video_{video_id}.mp4')
    output_path = os.path.join(settings.MEDIA_ROOT, "subtitles", f'subtitles_{video_id}.srt')

    # Run ccextractor to generate subtitles file
    ccextractor_command = f'"****path****" "{input_path}" -o "{output_path}"'
    try:
        subprocess.run(ccextractor_command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"Error running ccextractor: {e}")
        return "Error running ccextractor"

    # Processcessing generated subtitles file
    with open(output_path, 'r') as subtitle_file:
        subtitle_text = subtitle_file.read()
        subtitle_entries = subtitle_text.split('\n\n')
        for entry in subtitle_entries:
            lines = entry.split('\n')
            if len(lines) >= 3:
                sequence = lines[0]
                time_range = lines[1]
                start_time, end_time = parse_time_range(time_range)
                content = '\n'.join(lines[2:])
                content = content.strip()
                store_subtitle_in_dynamodb(video_id, start_time, content, end_time)

    video.save()
    return "Processing completed successfully"

def store_subtitle_in_dynamodb(video_id, start_time, content, end_time):
    aws_access_key_id = '******'
    aws_secret_access_key = '******'
    region_name = '******'

    dynamodb = boto3.client('dynamodb', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region_name)

    table_name = 'subtitles'
    item = {
        'video_id': {'S': str(video_id)},
        'start_time': {'S': start_time},
        'content': {'S': content},
        'end_time': {'S': end_time},
    }

    dynamodb.put_item(TableName=table_name, Item=item)
