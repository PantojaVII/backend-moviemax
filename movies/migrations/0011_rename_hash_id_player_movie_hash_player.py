# Generated by Django 4.2.7 on 2023-11-21 19:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0010_movie_hash_id_player'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movie',
            old_name='hash_id_player',
            new_name='hash_player',
        ),
    ]
