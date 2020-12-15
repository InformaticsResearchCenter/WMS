# Generated by Django 3.1 on 2020-12-05 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WMS', '0007_auto_20201205_1147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='borrow',
            name='id',
            field=models.TextField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='borrowdata',
            name='id',
            field=models.TextField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='costumerreturn',
            name='id',
            field=models.TextField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='costumerreturndata',
            name='id',
            field=models.TextField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='inbound',
            name='id',
            field=models.TextField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='inbounddata',
            name='id',
            field=models.TextField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='item',
            name='id',
            field=models.TextField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='itemdata',
            name='id',
            field=models.TextField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='outbound',
            name='id',
            field=models.TextField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='outbounddata',
            name='id',
            field=models.TextField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='id',
            field=models.TextField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='id',
            field=models.TextField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='supplierreturn',
            name='id',
            field=models.TextField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='supplierreturndata',
            name='id',
            field=models.TextField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='usergroup',
            name='id',
            field=models.TextField(primary_key=True, serialize=False),
        ),
    ]