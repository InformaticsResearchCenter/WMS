# Generated by Django 3.1 on 2021-02-10 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WMS', '0006_auto_20210208_1443'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='deleted',
            field=models.CharField(default=0, max_length=1),
        ),
        migrations.AlterField(
            model_name='log',
            name='detail',
            field=models.CharField(choices=[('0', 'None'), ('1', 'In'), ('2', 'Move'), ('3', 'Found'), ('4', 'Customer Return'), ('5', 'Borrowed'), ('6', 'Return Borrow')], default=0, max_length=2),
        ),
    ]