# Generated by Django 4.2.7 on 2023-12-07 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('series', '0007_serie_coverone_serie_covertwo_serie_highlight_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='serie',
            name='rating',
            field=models.CharField(default=0, max_length=3),
        ),
    ]