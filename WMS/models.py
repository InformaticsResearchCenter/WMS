from django.db import models


class Category(models.Model):
    categoryid = models.IntegerField(primary_key=True)
    category = models.TextField()

    class Meta:
        db_table = 'category'


class Item(models.Model):
    itemid = models.IntegerField(primary_key=True)
    name = models.TextField()
    detail = models.TextField()
    subcategoryid = models.ForeignKey(
        'Subcategory', models.DO_NOTHING, db_column='subcategoryid')

    class Meta:
        db_table = 'item'


class Itemdata(models.Model):
    itemdataid = models.IntegerField(primary_key=True)
    itemid = models.ForeignKey(Item, models.DO_NOTHING, db_column='itemid')
    dateofentry = models.DateField()
    outdate = models.DateField()
    binlocation = models.IntegerField()
    supplierid = models.ForeignKey(
        'Supplier', models.DO_NOTHING, db_column='supplierid')
    price = models.IntegerField()

    class Meta:
        db_table = 'itemdata'


class Role(models.Model):
    roleid = models.CharField(primary_key=True, max_length=3)
    role = models.CharField(max_length=10)

    class Meta:
        db_table = 'role'


class Subcategory(models.Model):
    subcategoryid = models.IntegerField(primary_key=True)
    subcategory = models.TextField()
    categoryid = models.ForeignKey(
        Category, models.DO_NOTHING, db_column='categoryid')

    class Meta:
        db_table = 'subcategory'


class Supplier(models.Model):
    supplierid = models.IntegerField(primary_key=True)
    companyname = models.TextField()
    address = models.TextField()
    phonenumber = models.TextField()
    email = models.TextField()

    class Meta:
        db_table = 'supplier'


class Userdata(models.Model):
    userid = models.IntegerField(primary_key=True)
    username = models.CharField(unique=True, max_length=50)
    password = models.CharField(max_length=50)
    roleid = models.ForeignKey(Role, models.DO_NOTHING, db_column='roleid')
    name = models.CharField(max_length=100)
    address = models.TextField()
    phonenumber = models.CharField(unique=True, max_length=14)
    email = models.CharField(unique=True, max_length=14)

    class Meta:
        db_table = 'userdata'
