# Generated by Django 3.1 on 2020-11-25 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WMS', '0005_auto_20201124_2010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='costumerreturn',
            name='status',
            field=models.CharField(choices=[('1', 'Open document'), ('2', 'Document ready'), ('3', 'Complete')], default=1, max_length=2),
        ),
    ]
