# Generated by Django 2.2.5 on 2021-07-28 13:39

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_auto_20210727_0003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='JPEG', keep_meta=True, quality=95, size=[1024, 1024], upload_to='avatars'),
        ),
    ]
