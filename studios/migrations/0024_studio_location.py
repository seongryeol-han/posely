# Generated by Django 2.2.5 on 2021-09-15 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studios', '0023_auto_20210907_1531'),
    ]

    operations = [
        migrations.AddField(
            model_name='studio',
            name='location',
            field=models.CharField(blank=True, max_length=140),
        ),
    ]
