# Generated by Django 3.1 on 2021-01-16 00:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DjangoSession',
            fields=[
                ('session_key', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('session_data', models.TextField()),
                ('expire_date', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_session',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SequencesSequence',
            fields=[
                ('name', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('last', models.IntegerField()),
            ],
            options={
                'db_table': 'sequences_sequence',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='NULL', max_length=50)),
                ('address', models.TextField(default='NULL')),
                ('phoneNumber', models.CharField(default='NULL', max_length=13)),
                ('postalCode', models.CharField(default='NULL', max_length=10)),
                ('districts', models.CharField(default='NULL', max_length=50)),
                ('city', models.CharField(default='NULL', max_length=50)),
                ('province', models.CharField(default='NULL', max_length=50)),
                ('username', models.CharField(max_length=50, null=True, unique=True)),
                ('password', models.CharField(max_length=50, null=True)),
                ('deleted', models.CharField(default=0, max_length=1)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Binlocation',
            fields=[
                ('id', models.CharField(default='NULL', max_length=5, primary_key=True, serialize=False)),
                ('deleted', models.CharField(default=0, max_length=1)),
                ('capacity', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Borrow',
            fields=[
                ('name', models.CharField(default='NULL', max_length=50)),
                ('phoneNumber', models.CharField(default='NULL', max_length=13)),
                ('id', models.TextField(primary_key=True, serialize=False)),
                ('deleted', models.CharField(default=0, max_length=1)),
                ('date', models.DateField(default='1000-10-10')),
                ('status', models.CharField(choices=[('1', 'Open document'), ('2', 'Document ready'), ('3', 'Complete'), ('4', 'Returned')], default=1, max_length=2)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.TextField(primary_key=True, serialize=False)),
                ('deleted', models.CharField(default=0, max_length=1)),
                ('category', models.CharField(default='NULL', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='CostumerReturn',
            fields=[
                ('id', models.TextField(primary_key=True, serialize=False)),
                ('deleted', models.CharField(default=0, max_length=1)),
                ('date', models.DateField(default='1000-10-10')),
                ('status', models.CharField(choices=[('1', 'Open document'), ('2', 'Document ready'), ('3', 'Complete')], default=1, max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('name', models.CharField(default='NULL', max_length=50)),
                ('address', models.TextField(default='NULL')),
                ('phoneNumber', models.CharField(default='NULL', max_length=13)),
                ('postalCode', models.CharField(default='NULL', max_length=10)),
                ('districts', models.CharField(default='NULL', max_length=50)),
                ('city', models.CharField(default='NULL', max_length=50)),
                ('province', models.CharField(default='NULL', max_length=50)),
                ('id', models.TextField(primary_key=True, serialize=False)),
                ('deleted', models.CharField(default=0, max_length=1)),
                ('email', models.CharField(default='NULL', max_length=50)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Inbound',
            fields=[
                ('id', models.TextField(primary_key=True, serialize=False)),
                ('deleted', models.CharField(default=0, max_length=1)),
                ('date', models.DateField(default='1000-10-10')),
                ('status', models.CharField(choices=[('1', 'Open document'), ('2', 'Complete with reject'), ('3', 'Complete')], default=1, max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='InboundData',
            fields=[
                ('id', models.TextField(primary_key=True, serialize=False)),
                ('deleted', models.CharField(default=0, max_length=1)),
                ('quantity', models.IntegerField(default=0)),
                ('reject', models.IntegerField(default=0)),
                ('rejectCounter', models.IntegerField(default=0)),
                ('inbound', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='WMS.inbound')),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.TextField(primary_key=True, serialize=False)),
                ('deleted', models.CharField(default=0, max_length=1)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Outbound',
            fields=[
                ('id', models.TextField(primary_key=True, serialize=False)),
                ('deleted', models.CharField(default=0, max_length=1)),
                ('date', models.DateField(default='1000-10-10')),
                ('status', models.CharField(choices=[('1', 'Open document'), ('2', 'Document ready'), ('3', 'Complete')], default=1, max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('role', models.CharField(choices=[('OPR', 'OPERATOR'), ('ADM', 'ADMINISTRATOR'), ('MAN', 'MANAGER'), ('NON', 'unidentified')], max_length=3, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='SupplierReturn',
            fields=[
                ('id', models.TextField(primary_key=True, serialize=False)),
                ('deleted', models.CharField(default=0, max_length=1)),
                ('date', models.DateField(default='1000-10-10')),
                ('status', models.CharField(choices=[('1', 'Open document'), ('2', 'Complete')], default=1, max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='UserGroup',
            fields=[
                ('name', models.CharField(default='NULL', max_length=50)),
                ('address', models.TextField(default='NULL')),
                ('phoneNumber', models.CharField(default='NULL', max_length=13)),
                ('postalCode', models.CharField(default='NULL', max_length=10)),
                ('districts', models.CharField(default='NULL', max_length=50)),
                ('city', models.CharField(default='NULL', max_length=50)),
                ('province', models.CharField(default='NULL', max_length=50)),
                ('id', models.TextField(primary_key=True, serialize=False)),
                ('limit', models.DateField(default='1000-10-10')),
                ('email', models.EmailField(max_length=254, null=True, unique=True)),
                ('password', models.CharField(max_length=100, null=True)),
                ('token', models.CharField(max_length=100, null=True)),
                ('active', models.CharField(default=0, max_length=1)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='NULL', max_length=50)),
                ('address', models.TextField(default='NULL')),
                ('phoneNumber', models.CharField(default='NULL', max_length=13)),
                ('postalCode', models.CharField(default='NULL', max_length=10)),
                ('districts', models.CharField(default='NULL', max_length=50)),
                ('city', models.CharField(default='NULL', max_length=50)),
                ('province', models.CharField(default='NULL', max_length=50)),
                ('deleted', models.CharField(default=0, max_length=1)),
                ('username', models.CharField(max_length=50, null=True, unique=True)),
                ('password', models.CharField(max_length=50, null=True)),
                ('role', models.ForeignKey(default='NON', null=True, on_delete=django.db.models.deletion.CASCADE, to='WMS.role')),
                ('userGroup', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='WMS.usergroup')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SupplierReturnData',
            fields=[
                ('id', models.TextField(primary_key=True, serialize=False)),
                ('deleted', models.CharField(default=0, max_length=1)),
                ('quantity', models.IntegerField(default=0)),
                ('reject', models.IntegerField(default=0)),
                ('item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='WMS.item')),
                ('supplierReturn', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='WMS.supplierreturn')),
                ('userGroup', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='WMS.usergroup')),
            ],
        ),
        migrations.AddField(
            model_name='supplierreturn',
            name='confirm',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='srConfirm', to='WMS.user'),
        ),
        migrations.AddField(
            model_name='supplierreturn',
            name='create',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='srCreate', to='WMS.user'),
        ),
        migrations.AddField(
            model_name='supplierreturn',
            name='inbound',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='WMS.inbound'),
        ),
        migrations.AddField(
            model_name='supplierreturn',
            name='userGroup',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='WMS.usergroup'),
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('name', models.CharField(default='NULL', max_length=50)),
                ('address', models.TextField(default='NULL')),
                ('phoneNumber', models.CharField(default='NULL', max_length=13)),
                ('postalCode', models.CharField(default='NULL', max_length=10)),
                ('districts', models.CharField(default='NULL', max_length=50)),
                ('city', models.CharField(default='NULL', max_length=50)),
                ('province', models.CharField(default='NULL', max_length=50)),
                ('id', models.TextField(primary_key=True, serialize=False)),
                ('deleted', models.CharField(default=0, max_length=1)),
                ('email', models.CharField(default='NULL', max_length=50)),
                ('userGroup', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='WMS.usergroup')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('id', models.TextField(primary_key=True, serialize=False)),
                ('deleted', models.CharField(default=0, max_length=1)),
                ('subcategory', models.CharField(default='NULL', max_length=50)),
                ('size', models.CharField(max_length=50, null=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='WMS.category')),
                ('userGroup', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='WMS.usergroup')),
            ],
        ),
        migrations.CreateModel(
            name='Rack',
            fields=[
                ('deleted', models.CharField(default=0, max_length=1)),
                ('id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('userGroup', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='WMS.usergroup')),
            ],
        ),
        migrations.CreateModel(
            name='OutboundData',
            fields=[
                ('id', models.TextField(primary_key=True, serialize=False)),
                ('deleted', models.CharField(default=0, max_length=1)),
                ('quantity', models.IntegerField(default=0)),
                ('item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='WMS.item')),
                ('outbound', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='WMS.outbound')),
                ('userGroup', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='WMS.usergroup')),
            ],
        ),
        migrations.AddField(
            model_name='outbound',
            name='confirm',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='oConfirm', to='WMS.user'),
        ),
        migrations.AddField(
            model_name='outbound',
            name='create',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='oCreate', to='WMS.user'),
        ),
        migrations.AddField(
            model_name='outbound',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='WMS.customer'),
        ),
        migrations.AddField(
            model_name='outbound',
            name='userGroup',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='WMS.usergroup'),
        ),
        migrations.CreateModel(
            name='ItemData',
            fields=[
                ('id', models.TextField(primary_key=True, serialize=False)),
                ('deleted', models.CharField(default=0, max_length=1)),
                ('status', models.CharField(choices=[('0', 'unidentified'), ('1', 'avaible'), ('2', 'sold'), ('3', 'borrowed'), ('4', 'broken'), ('5', 'lost')], default=0, max_length=2)),
                ('binlocation', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='WMS.binlocation')),
                ('borrow', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='WMS.borrow')),
                ('inbound', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='WMS.inbounddata')),
                ('outbound', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='WMS.outbound')),
                ('returnData', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='WMS.supplierreturndata')),
                ('userGroup', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='WMS.usergroup')),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='subcategory',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='WMS.subcategory'),
        ),
        migrations.AddField(
            model_name='item',
            name='userGroup',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='WMS.usergroup'),
        ),
        migrations.AddField(
            model_name='inbounddata',
            name='item',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='WMS.item'),
        ),
        migrations.AddField(
            model_name='inbounddata',
            name='userGroup',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='WMS.usergroup'),
        ),
        migrations.AddField(
            model_name='inbound',
            name='confirm',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='iConfirm', to='WMS.user'),
        ),
        migrations.AddField(
            model_name='inbound',
            name='create',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='iCreate', to='WMS.user'),
        ),
        migrations.AddField(
            model_name='inbound',
            name='supplier',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='WMS.supplier'),
        ),
        migrations.AddField(
            model_name='inbound',
            name='userGroup',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='WMS.usergroup'),
        ),
        migrations.AddField(
            model_name='customer',
            name='userGroup',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='WMS.usergroup'),
        ),
        migrations.CreateModel(
            name='CostumerReturnData',
            fields=[
                ('id', models.TextField(primary_key=True, serialize=False)),
                ('deleted', models.CharField(default=0, max_length=1)),
                ('quantity', models.IntegerField(default=0)),
                ('reject', models.IntegerField(default=0)),
                ('costumerReturn', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='WMS.costumerreturn')),
                ('item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='WMS.item')),
                ('userGroup', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='WMS.usergroup')),
            ],
        ),
        migrations.AddField(
            model_name='costumerreturn',
            name='confirm',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='crConfirm', to='WMS.user'),
        ),
        migrations.AddField(
            model_name='costumerreturn',
            name='create',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='crCreate', to='WMS.user'),
        ),
        migrations.AddField(
            model_name='costumerreturn',
            name='outbound',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='WMS.outbound'),
        ),
        migrations.AddField(
            model_name='costumerreturn',
            name='userGroup',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='WMS.usergroup'),
        ),
        migrations.AddField(
            model_name='category',
            name='userGroup',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='WMS.usergroup'),
        ),
        migrations.CreateModel(
            name='BorrowData',
            fields=[
                ('id', models.TextField(primary_key=True, serialize=False)),
                ('deleted', models.CharField(default=0, max_length=1)),
                ('quantity', models.IntegerField(default=0)),
                ('borrow', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='WMS.borrow')),
                ('item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='WMS.item')),
                ('userGroup', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='WMS.usergroup')),
            ],
        ),
        migrations.AddField(
            model_name='borrow',
            name='confirm',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bConfirm', to='WMS.user'),
        ),
        migrations.AddField(
            model_name='borrow',
            name='create',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bCreate', to='WMS.user'),
        ),
        migrations.AddField(
            model_name='borrow',
            name='userGroup',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='WMS.usergroup'),
        ),
        migrations.AddField(
            model_name='binlocation',
            name='rack',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='WMS.rack'),
        ),
        migrations.AddField(
            model_name='binlocation',
            name='userGroup',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='WMS.usergroup'),
        ),
    ]
