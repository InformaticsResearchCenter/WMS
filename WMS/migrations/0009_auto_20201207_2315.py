# Generated by Django 3.1 on 2020-12-07 16:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('WMS', '0008_auto_20201205_1152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemdata',
            name='inbound',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='WMS.inbound'),
        ),
    ]