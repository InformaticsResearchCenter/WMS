# Generated by Django 3.1 on 2021-01-16 00:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WMS', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='admin',
            name='village',
            field=models.CharField(default='NULL', max_length=50),
        ),
        migrations.AddField(
            model_name='customer',
            name='village',
            field=models.CharField(default='NULL', max_length=50),
        ),
        migrations.AddField(
            model_name='supplier',
            name='village',
            field=models.CharField(default='NULL', max_length=50),
        ),
        migrations.AddField(
            model_name='user',
            name='village',
            field=models.CharField(default='NULL', max_length=50),
        ),
        migrations.AddField(
            model_name='usergroup',
            name='addressCompany',
            field=models.TextField(default='NULL'),
        ),
        migrations.AddField(
            model_name='usergroup',
            name='imageCompany',
            field=models.CharField(default='NULL', max_length=100),
        ),
        migrations.AddField(
            model_name='usergroup',
            name='namaOperator',
            field=models.CharField(default='NULL', max_length=50),
        ),
        migrations.AddField(
            model_name='usergroup',
            name='nameCompany',
            field=models.CharField(default='NULL', max_length=50),
        ),
        migrations.AddField(
            model_name='usergroup',
            name='profileOperator',
            field=models.CharField(default='NULL', max_length=100),
        ),
        migrations.AddField(
            model_name='usergroup',
            name='village',
            field=models.CharField(default='NULL', max_length=50),
        ),
    ]
