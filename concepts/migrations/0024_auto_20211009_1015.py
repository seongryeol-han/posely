# Generated by Django 2.2.5 on 2021-10-09 01:15

import concepts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('concepts', '0023_auto_20210923_1512'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='random_int',
            field=models.CharField(blank=True, default=concepts.models.Photo.random_string, max_length=6),
        ),
    ]
