# Generated by Django 4.2.7 on 2024-02-07 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('series', '0016_alter_episode_player'),
    ]

    operations = [
        migrations.AlterField(
            model_name='episode',
            name='playerURL',
            field=models.URLField(blank=True),
        ),
    ]
