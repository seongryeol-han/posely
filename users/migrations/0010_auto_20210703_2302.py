# Generated by Django 2.2.5 on 2021-07-03 14:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_user_has_studio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='has_studio',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='has_studio', to='studios.Studio'),
        ),
    ]
