# Generated by Django 2.2.5 on 2021-07-06 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('concepts', '0010_auto_20210706_2320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='concept',
            name='price',
            field=models.DecimalField(decimal_places=3, max_digits=6),
        ),
    ]
