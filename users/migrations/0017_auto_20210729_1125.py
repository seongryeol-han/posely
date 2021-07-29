# Generated by Django 2.2.5 on 2021-07-29 02:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_auto_20210728_2239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='nickname',
            field=models.CharField(error_messages={'unique': '이미 존재하는 닉네임입니다.'}, max_length=30, unique=True),
        ),
    ]