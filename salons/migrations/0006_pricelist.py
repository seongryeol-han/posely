# Generated by Django 2.2.5 on 2021-10-15 14:17

from django.db import migrations, models
import django.db.models.deletion
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('salons', '0005_auto_20211011_1216'),
    ]

    operations = [
        migrations.CreateModel(
            name='PriceList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('file', django_resized.forms.ResizedImageField(crop=None, force_format='JPEG', keep_meta=True, quality=95, size=[1024, 1024], upload_to='salon_pricelist')),
                ('salon', models.ForeignKey(blank=True, default='', on_delete=django.db.models.deletion.CASCADE, related_name='pricelists', to='salons.Salon')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]