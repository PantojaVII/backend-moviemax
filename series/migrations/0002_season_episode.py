# Generated by Django 4.2.7 on 2023-11-09 16:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('series', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('season', models.PositiveSmallIntegerField()),
                ('synopsis', models.TextField()),
                ('release_date', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('serie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='series.series')),
            ],
        ),
        migrations.CreateModel(
            name='Episode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_episode', models.PositiveSmallIntegerField()),
                ('name', models.CharField(max_length=100)),
                ('duration', models.DurationField()),
                ('synopsis', models.TextField()),
                ('player', models.URLField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='series.season')),
            ],
        ),
    ]
