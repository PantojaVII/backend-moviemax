# Generated by Django 4.2.7 on 2023-11-24 19:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0018_alter_movie_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='coverOne',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='coverTwo',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='highlight',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='player',
        ),
    ]
