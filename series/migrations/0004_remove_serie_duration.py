# Generated by Django 4.2.7 on 2023-11-09 19:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('series', '0003_rename_series_serie'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='serie',
            name='duration',
        ),
    ]
