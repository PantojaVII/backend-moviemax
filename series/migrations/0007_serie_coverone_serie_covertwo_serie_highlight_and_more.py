# Generated by Django 4.2.7 on 2023-12-07 18:18

from django.db import migrations, models
import series.models


class Migration(migrations.Migration):

    dependencies = [
        ('series', '0006_serie_info'),
    ]

    operations = [
        migrations.AddField(
            model_name='serie',
            name='coverOne',
            field=models.FileField(default=0, upload_to=series.models.movie_upload_path),
        ),
        migrations.AddField(
            model_name='serie',
            name='coverTwo',
            field=models.FileField(default=0, upload_to=series.models.movie_upload_path),
        ),
        migrations.AddField(
            model_name='serie',
            name='highlight',
            field=models.FileField(default=0, upload_to=series.models.movie_upload_path),
        ),
        migrations.AlterField(
            model_name='serie',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
