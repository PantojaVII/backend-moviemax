# Generated by Django 4.2.7 on 2024-02-22 22:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0031_alter_movie_player'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movie',
            old_name='playerURL',
            new_name='player_name',
        ),
    ]
