# Generated by Django 2.2.5 on 2021-09-20 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('concepts', '0020_photo_random_int'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='random_int',
            field=models.CharField(blank=True, default='random_string', max_length=6),
        ),
    ]
