# Generated by Django 4.2.7 on 2024-02-07 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0025_movie_hashed_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='playerURL',
            field=models.URLField(default=False),
        ),
    ]
