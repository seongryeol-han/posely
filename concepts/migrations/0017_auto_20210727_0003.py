# Generated by Django 2.2.5 on 2021-07-26 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('concepts', '0016_auto_20210725_0938'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='file',
            field=models.ImageField(upload_to='concept_photos'),
        ),
    ]
