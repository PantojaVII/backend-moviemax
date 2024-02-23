# Generated by Django 4.2.7 on 2024-02-22 23:36

from django.db import migrations, models
import series.models


class Migration(migrations.Migration):

    dependencies = [
        ('series', '0020_remove_episode_playerurl_episode_player_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='episode',
            name='hashed_id',
            field=models.CharField(blank=True, max_length=15, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='episode',
            name='player',
            field=models.FileField(blank=True, null=True, upload_to=series.models.episode_upload_path),
        ),
        migrations.AlterField(
            model_name='season',
            name='hashed_id',
            field=models.CharField(blank=True, max_length=15, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='serie',
            name='hashed_id',
            field=models.CharField(blank=True, max_length=15, null=True, unique=True),
        ),
    ]
