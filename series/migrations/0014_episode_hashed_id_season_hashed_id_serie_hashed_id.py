# Generated by Django 4.2.7 on 2024-01-12 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('series', '0013_alter_serie_genres'),
    ]

    operations = [
        migrations.AddField(
            model_name='episode',
            name='hashed_id',
            field=models.CharField(blank=True, max_length=64, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='season',
            name='hashed_id',
            field=models.CharField(blank=True, max_length=64, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='serie',
            name='hashed_id',
            field=models.CharField(blank=True, max_length=64, null=True, unique=True),
        ),
    ]