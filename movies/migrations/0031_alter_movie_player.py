# Generated by Django 4.2.7 on 2024-02-22 21:31

from django.db import migrations, models
import movies.models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0030_alter_movie_playerurl'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='player',
            field=models.FileField(blank=True, null=True),
        ),
    ]
