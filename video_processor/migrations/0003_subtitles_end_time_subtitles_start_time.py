# Generated by Django 5.0 on 2023-12-17 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video_processor', '0002_remove_subtitles_end_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='subtitles',
            name='end_time',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='subtitles',
            name='start_time',
            field=models.FloatField(null=True),
        ),
    ]
