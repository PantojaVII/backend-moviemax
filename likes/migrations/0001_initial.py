# Generated by Django 4.2.7 on 2023-11-09 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Likes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.PositiveSmallIntegerField(choices=[(1, 'Filme'), (2, 'Série')])),
                ('content_id', models.PositiveIntegerField()),
            ],
        ),
    ]
