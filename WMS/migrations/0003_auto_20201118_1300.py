# Generated by Django 3.1 on 2020-11-18 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WMS', '0002_admin'),
    ]

    operations = [
        migrations.AddField(
            model_name='usergroup',
            name='email',
            field=models.EmailField(max_length=254, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='usergroup',
            name='password',
            field=models.CharField(max_length=100, null=True),
        ),
    ]