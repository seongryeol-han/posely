# Generated by Django 2.2.5 on 2021-09-20 00:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('concepts', '0018_auto_20210728_2239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='caption',
            field=models.CharField(blank=True, default='', max_length=80),
        ),
    ]