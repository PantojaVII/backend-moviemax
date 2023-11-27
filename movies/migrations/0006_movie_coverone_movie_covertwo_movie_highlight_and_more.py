# Generated by Django 4.2.7 on 2023-11-21 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0005_delete_genre_alter_movie_genres'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='coverOne',
            field=models.URLField(default=False),
        ),
        migrations.AddField(
            model_name='movie',
            name='coverTwo',
            field=models.URLField(default=False),
        ),
        migrations.AddField(
            model_name='movie',
            name='highlight',
            field=models.URLField(default=False),
        ),
        migrations.AddField(
            model_name='movie',
            name='playerTrailer',
            field=models.URLField(default=False),
        ),
    ]