# Generated by Django 4.2.7 on 2023-11-21 18:12

import autoslug.fields
from django.db import migrations, models
import movies.models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0006_movie_coverone_movie_covertwo_movie_highlight_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='slug',
            field=autoslug.fields.AutoSlugField(blank=True, editable=False, null=True, populate_from='name', unique=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='player',
            field=models.FileField(upload_to=movies.models.movie_upload_path),
        ),
    ]
