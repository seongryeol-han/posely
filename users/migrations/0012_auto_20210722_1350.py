# Generated by Django 2.2.5 on 2021-07-22 04:50

import core.managers
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_auto_20210703_2344'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', core.managers.CustomUserManager()),
            ],
        ),
    ]
