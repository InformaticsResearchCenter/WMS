# Generated by Django 3.1 on 2021-01-14 06:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('WMS', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='kecamatan',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='kota',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='provinsi',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='rt',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='rw',
        ),
        migrations.RemoveField(
            model_name='supplier',
            name='kecamatan',
        ),
        migrations.RemoveField(
            model_name='supplier',
            name='kota',
        ),
        migrations.RemoveField(
            model_name='supplier',
            name='provinsi',
        ),
        migrations.RemoveField(
            model_name='supplier',
            name='rt',
        ),
        migrations.RemoveField(
            model_name='supplier',
            name='rw',
        ),
    ]
