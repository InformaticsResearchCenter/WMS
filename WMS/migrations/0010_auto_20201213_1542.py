# Generated by Django 3.0.9 on 2020-12-13 08:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('WMS', '0009_auto_20201207_2315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemdata',
            name='inbound',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='WMS.InboundData'),
        ),
    ]