# Generated by Django 2.2.5 on 2021-07-25 00:38

from django.db import migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('concepts', '0015_auto_20210707_0004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='file',
            field=imagekit.models.fields.ProcessedImageField(upload_to='concept_photos'),
        ),
    ]
