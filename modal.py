# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Binlocation(models.Model):
    id = models.TextField(primary_key=True)
    rackid = models.ForeignKey('Rack', models.DO_NOTHING, db_column='rackid')
    capacity = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'binlocation'


class Category(models.Model):
    id = models.TextField(primary_key=True)
    name = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'category'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Inbounddata(models.Model):
    id = models.TextField(primary_key=True)
    supplierid = models.ForeignKey('Supplier', models.DO_NOTHING, db_column='supplierid')
    status = models.CharField(max_length=20)
    date = models.DateField()
    confirm = models.ForeignKey('Userdata', models.DO_NOTHING, db_column='confirm', blank=True, null=True)
    created = models.ForeignKey('Userdata', models.DO_NOTHING, db_column='created', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'inbounddata'


class Item(models.Model):
    id = models.TextField(primary_key=True)
    name = models.CharField(max_length=50)
    subcategoryid = models.ForeignKey('Subcategory', models.DO_NOTHING, db_column='subcategoryid')

    class Meta:
        managed = False
        db_table = 'item'


class Itembatch(models.Model):
    id = models.TextField(primary_key=True)
    binid = models.ForeignKey(Binlocation, models.DO_NOTHING, db_column='binid', blank=True, null=True)
    entry = models.DateField(blank=True, null=True)
    out = models.DateField(blank=True, null=True)
    itemdataid = models.ForeignKey('Itemdata', models.DO_NOTHING, db_column='itemdataid')
    qr_code = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'itembatch'


class Itemdata(models.Model):
    id = models.TextField(primary_key=True)
    inboundid = models.ForeignKey(Inbounddata, models.DO_NOTHING, db_column='inboundid')
    itemid = models.ForeignKey(Item, models.DO_NOTHING, db_column='itemid')
    quantity = models.IntegerField()
    pass_field = models.IntegerField(db_column='pass')  # Field renamed because it was a Python reserved word.
    reject = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'itemdata'


class Outbound(models.Model):
    id = models.TextField(primary_key=True)
    customername = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phonenumber = models.TextField()
    date = models.DateField()
    status = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'outbound'


class Outbounddata(models.Model):
    id = models.TextField(primary_key=True)
    itemid = models.ForeignKey(Item, models.DO_NOTHING, db_column='itemid')
    quantity = models.IntegerField()
    outboundid = models.ForeignKey(Outbound, models.DO_NOTHING, db_column='outboundid')

    class Meta:
        managed = False
        db_table = 'outbounddata'


class Rack(models.Model):
    id = models.TextField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'rack'


class Returndata(models.Model):
    id = models.TextField(primary_key=True)
    inboundid = models.TextField()
    itemid = models.ForeignKey(Item, models.DO_NOTHING, db_column='itemid')
    status = models.CharField(max_length=20)
    date = models.DateField()
    confirm = models.ForeignKey('Userdata', models.DO_NOTHING, db_column='confirm', blank=True, null=True)
    created = models.ForeignKey('Userdata', models.DO_NOTHING, db_column='created', blank=True, null=True)
    itemdataid = models.ForeignKey(Itemdata, models.DO_NOTHING, db_column='itemdataid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'returndata'


class Role(models.Model):
    roleid = models.CharField(primary_key=True, max_length=3)
    role = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'role'


class SequencesSequence(models.Model):
    name = models.CharField(primary_key=True, max_length=100)
    last = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'sequences_sequence'


class Subcategory(models.Model):
    id = models.TextField(primary_key=True)
    name = models.CharField(max_length=30)
    categoryid = models.ForeignKey(Category, models.DO_NOTHING, db_column='categoryid')

    class Meta:
        managed = False
        db_table = 'subcategory'


class Supplier(models.Model):
    id = models.TextField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=13)
    address = models.CharField(max_length=100)
    postalcode = models.CharField(max_length=6)

    class Meta:
        managed = False
        db_table = 'supplier'


class Userdata(models.Model):
    id = models.TextField(primary_key=True)
    username = models.CharField(max_length=50, blank=True, null=True)
    password = models.CharField(max_length=50, blank=True, null=True)
    roleid = models.ForeignKey(Role, models.DO_NOTHING, db_column='roleid', blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    phonenumber = models.CharField(max_length=13, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'userdata'
