# Generated by Django 4.2.7 on 2023-12-07 18:43

from django.db import migrations, models
import series.models


class Migration(migrations.Migration):

    dependencies = [
        ('series', '0008_serie_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='episode',
            name='player',
            field=models.FileField(upload_to=series.models.movie_upload_path),
        ),
    ]
