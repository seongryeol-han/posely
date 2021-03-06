# Generated by Django 2.2.5 on 2021-05-09 12:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Concept',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=30)),
                ('concept_description', models.TextField()),
                ('price', models.DecimalField(decimal_places=0, max_digits=6)),
                ('service_config', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('caption', models.CharField(default='', max_length=80)),
                ('file', models.ImageField(upload_to='concept_photos')),
                ('concept', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='concepts.Concept')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
