# Generated by Django 2.2.5 on 2021-06-07 13:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('studios', '0002_auto_20210607_2241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studio',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='studios', to=settings.AUTH_USER_MODEL),
        ),
    ]
