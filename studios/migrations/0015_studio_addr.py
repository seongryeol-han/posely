# Generated by Django 2.2.5 on 2021-07-14 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studios', '0014_auto_20210711_2305'),
    ]

    operations = [
        migrations.AddField(
            model_name='studio',
            name='addr',
            field=models.CharField(blank=True, max_length=140),
        ),
    ]
