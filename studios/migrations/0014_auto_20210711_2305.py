# Generated by Django 2.2.5 on 2021-07-11 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studios', '0013_auto_20210708_2254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studio',
            name='studio_lat',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='studio',
            name='studio_lng',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
