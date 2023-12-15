# Generated by Django 4.2.7 on 2023-12-08 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('series', '0010_serie_playertrailer_alter_episode_player'),
    ]

    operations = [
        migrations.AddField(
            model_name='serie',
            name='age_groups',
            field=models.IntegerField(choices=[(1, 'LIVRE'), (2, '+10'), (3, '+12'), (4, '+16'), (5, '+18')], default=1),
        ),
    ]
