# Generated by Django 3.1 on 2021-01-14 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WMS', '0002_auto_20210114_1347'),
    ]

    operations = [
        migrations.AddField(
            model_name='admin',
            name='city',
            field=models.CharField(default='NULL', max_length=50),
        ),
        migrations.AddField(
            model_name='admin',
            name='districts',
            field=models.CharField(default='NULL', max_length=50),
        ),
        migrations.AddField(
            model_name='admin',
            name='province',
            field=models.CharField(default='NULL', max_length=50),
        ),
        migrations.AddField(
            model_name='customer',
            name='city',
            field=models.CharField(default='NULL', max_length=50),
        ),
        migrations.AddField(
            model_name='customer',
            name='districts',
            field=models.CharField(default='NULL', max_length=50),
        ),
        migrations.AddField(
            model_name='customer',
            name='province',
            field=models.CharField(default='NULL', max_length=50),
        ),
        migrations.AddField(
            model_name='supplier',
            name='city',
            field=models.CharField(default='NULL', max_length=50),
        ),
        migrations.AddField(
            model_name='supplier',
            name='districts',
            field=models.CharField(default='NULL', max_length=50),
        ),
        migrations.AddField(
            model_name='supplier',
            name='province',
            field=models.CharField(default='NULL', max_length=50),
        ),
        migrations.AddField(
            model_name='user',
            name='city',
            field=models.CharField(default='NULL', max_length=50),
        ),
        migrations.AddField(
            model_name='user',
            name='districts',
            field=models.CharField(default='NULL', max_length=50),
        ),
        migrations.AddField(
            model_name='user',
            name='province',
            field=models.CharField(default='NULL', max_length=50),
        ),
        migrations.AddField(
            model_name='usergroup',
            name='city',
            field=models.CharField(default='NULL', max_length=50),
        ),
        migrations.AddField(
            model_name='usergroup',
            name='districts',
            field=models.CharField(default='NULL', max_length=50),
        ),
        migrations.AddField(
            model_name='usergroup',
            name='province',
            field=models.CharField(default='NULL', max_length=50),
        ),
    ]