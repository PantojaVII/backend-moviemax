# Generated by Django 4.2.7 on 2023-11-21 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0009_remove_movie_hash_id_player'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='hash_id_player',
            field=models.CharField(blank=True, editable=False, max_length=64, null=True, unique=True),
        ),
    ]
