# Generated by Django 2.2.5 on 2021-09-21 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('concepts', '0021_auto_20210920_2141'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='button_filter',
            field=models.CharField(blank=True, default='', max_length=80),
        ),
    ]
