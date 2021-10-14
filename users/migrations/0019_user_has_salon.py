# Generated by Django 2.2.5 on 2021-10-14 12:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('salons', '0005_auto_20211011_1216'),
        ('users', '0018_user_salon'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='has_salon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='has_salon', to='salons.Salon'),
        ),
    ]
