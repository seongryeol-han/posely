# Generated by Django 2.2.5 on 2021-07-14 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studios', '0015_studio_addr'),
    ]

    operations = [
        migrations.AddField(
            model_name='studio',
            name='detail',
            field=models.CharField(blank=True, max_length=140),
        ),
    ]
