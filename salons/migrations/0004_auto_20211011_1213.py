# Generated by Django 2.2.5 on 2021-10-11 03:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salons', '0003_concept_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='concept',
            name='price',
            field=models.CharField(blank=True, default='', max_length=15),
        ),
    ]
