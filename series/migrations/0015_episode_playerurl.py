# Generated by Django 4.2.7 on 2024-02-07 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('series', '0014_episode_hashed_id_season_hashed_id_serie_hashed_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='episode',
            name='playerURL',
            field=models.URLField(default=False),
        ),
    ]