# Generated by Django 2.2.5 on 2021-07-26 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studios', '0020_auto_20210725_0938'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studio',
            name='studio_avatar',
            field=models.ImageField(blank=True, default='', null=True, upload_to='studio_photos'),
        ),
    ]
