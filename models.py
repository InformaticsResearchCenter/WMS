from django.db import models

class External(models.Model):
    name = models.CharField(max_length=50,default="NULL")
    address = models.TextField(default="NULL")
    phoneNumber = models.CharField(max_length=13,default="NULL")
    postalCode = models.CharField(max_length=10 ,default="NULL")

    class Meta:
        abstract = True

class Employee(models.Model):
    name = models.CharField(max_length=50,default="NULL")
    phoneNumber = models.CharField(max_length=13,default="NULL")

    class Meta:
        abstract = True

class Role(models.Model):
    role_choices = [
        ('OPR','OPERATOR'),
        ('ADM','ADMINISTRATOR'),
        ('MAN','MANAGER'),
        ('NON','unidentified')
    ]
    role = models.CharField(max_length=3, choices=role_choices, primary_key=True)
    
class UserGroup(External):
    limit = models.DateField(default="1000-10-10")

class Category(models.Model):
    userGroup = models.ForeignKey(UserGroup, on_delete=models.CASCADE, null=True)
    deleted = models.CharField(max_length=1, default=0)
    category = models.CharField(max_length=50, default="NULL")

class Subcategory(models.Model):
    userGroup = models.ForeignKey(UserGroup, on_delete=models.CASCADE, null=True)
    deleted = models.CharField(max_length=1, default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    subcategory = models.CharField(max_length=50, default="NULL")

class Item(models.Model):
    userGroup = models.ForeignKey(UserGroup, on_delete=models.CASCADE, null=True)
    deleted = models.CharField(max_length=1, default=0)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50)

class User(External):
    userGroup = models.ForeignKey(UserGroup, on_delete=models.CASCADE, null=True)
    deleted = models.CharField(max_length=1, default=0)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, default="NON")
    username = models.CharField(max_length=50, unique=True, null=True)
    password = models.CharField(max_length=50, null=True)

class Supplier(External):
    userGroup = models.ForeignKey(UserGroup, on_delete=models.CASCADE, null=True)
    deleted = models.CharField(max_length=1, default=0)
    email = models.CharField(max_length=50, default="NULL")

class Inbound(models.Model):
    status_choices = [
        ('1','Open document'),
        ('2','Complete with reject'),
        ('3','Complete'),
    ]
    userGroup = models.ForeignKey(UserGroup, on_delete=models.CASCADE, null=True)
    deleted = models.CharField(max_length=1, default=0)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True)
    date = models.DateField(default="1000-10-10")
    status = models.CharField(max_length=2, choices=status_choices, default=1)
    confirm = models.ForeignKey(User, related_name="iConfirm", on_delete=models.CASCADE, null=True)
    create = models.ForeignKey(User, related_name="iCreate", on_delete=models.CASCADE, null=True)

class InboundData(models.Model):
    userGroup = models.ForeignKey(UserGroup, on_delete=models.CASCADE, null=True)
    deleted = models.CharField(max_length=1, default=0)
    inbound = models.ForeignKey(Inbound, on_delete=models.CASCADE, null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=0)
    reject = models.IntegerField(default=0)
    rejectCounter = models.IntegerField(default=0)
    
    def condition(self):
        if self.rejectCounter > 0:
            return "REJECT"
        else:
            return "COMPLETE"

class Outbound(External):
    status_choices = [
        ('1','Open document'),
        ('2','Complete'),
    ]
    userGroup = models.ForeignKey(UserGroup, on_delete=models.CASCADE, null=True)
    deleted = models.CharField(max_length=1, default=0)
    date = models.DateField(default="1000-10-10")
    status = models.CharField(max_length=2, choices=status_choices, default=1)
    confirm = models.ForeignKey(User, related_name="oConfirm", on_delete=models.CASCADE, null=True)
    create = models.ForeignKey(User, related_name="oCreate", on_delete=models.CASCADE, null=True)

class OutboundData(models.Model):
    userGroup = models.ForeignKey(UserGroup, on_delete=models.CASCADE, null=True)
    deleted = models.CharField(max_length=1, default=0)
    outbound = models.ForeignKey(Outbound, on_delete=models.CASCADE, null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=0)
 
class Borrow(Employee):
    status_choices = [
        ('1','Open document'),
        ('2','Complete'),
        ('3','Returned')
    ]
    userGroup = models.ForeignKey(UserGroup, on_delete=models.CASCADE, null=True)
    deleted = models.CharField(max_length=1, default=0)
    date = models.DateField(default="1000-10-10")
    status = models.CharField(max_length=2, choices=status_choices, default=1)
    confirm = models.ForeignKey(User, related_name="bConfirm", on_delete=models.CASCADE, null=True)
    create = models.ForeignKey(User, related_name="bCreate", on_delete=models.CASCADE, null=True)

class BorrowData(models.Model):
    userGroup = models.ForeignKey(UserGroup, on_delete=models.CASCADE, null=True)
    deleted = models.CharField(max_length=1, default=0)
    borrow = models.ForeignKey(Borrow, on_delete=models.CASCADE, null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=0)

class SupplierReturn(models.Model):
    status_choices = [
        ('1','Open document'),
        ('2','Complete'),
    ]
    userGroup = models.ForeignKey(UserGroup, on_delete=models.CASCADE, null=True)
    deleted = models.CharField(max_length=1, default=0)
    inbound = models.ForeignKey(Inbound, on_delete=models.CASCADE, null=True)
    date = models.DateField(default="1000-10-10")
    status = models.CharField(max_length=2, choices=status_choices, default=1)
    confirm = models.ForeignKey(User, related_name="srConfirm", on_delete=models.CASCADE, null=True)
    create = models.ForeignKey(User, related_name="srCreate", on_delete=models.CASCADE, null=True)

class SupplierReturnData(models.Model):
    userGroup = models.ForeignKey(UserGroup, on_delete=models.CASCADE, null=True)
    deleted = models.CharField(max_length=1, default=0)
    supplierReturn = models.ForeignKey(SupplierReturn, on_delete=models.CASCADE, null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=0)
    reject = models.IntegerField(default=0)

class CostumerReturn(models.Model):
    status_choices = [
        ('1','Open document'),
        ('2','Complete'),
    ]
    userGroup = models.ForeignKey(UserGroup, on_delete=models.CASCADE, null=True)
    deleted = models.CharField(max_length=1, default=0)
    outbound = models.ForeignKey(Outbound, on_delete=models.CASCADE, null=True)
    date = models.DateField(default="1000-10-10")
    status = models.CharField(max_length=2, choices=status_choices, default=1)
    confirm = models.ForeignKey(User, related_name="crConfirm", on_delete=models.CASCADE, null=True)
    create = models.ForeignKey(User, related_name="crCreate", on_delete=models.CASCADE, null=True)

class costumerReturnData(models.Model):
    userGroup = models.ForeignKey(UserGroup, on_delete=models.CASCADE, null=True)
    deleted = models.CharField(max_length=1, default=0)
    costumerReturn = models.ForeignKey(CostumerReturn, on_delete=models.CASCADE, null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=0)
    reject = models.IntegerField(default=0)

class Rack(models.Model):
    userGroup = models.ForeignKey(UserGroup, on_delete=models.CASCADE, null=True)
    deleted = models.CharField(max_length=1, default=0)
    id = models.CharField(max_length=10, primary_key=True)

class Binlocation(models.Model):
    userGroup = models.ForeignKey(UserGroup, on_delete=models.CASCADE, null=True)
    deleted = models.CharField(max_length=1, default=0)
    rack = models.ForeignKey(Rack, on_delete=models.CASCADE, null=True)
    capacity = models.IntegerField(null=True)

class ItemData(models.Model):
    status_list=[
        ('0','unidentified'),
        ('1','sold'),
        ('2','avaible'),
        ('3','borrowed'),
        ('4','broken'),
        ('5','lost'),
    ]
    userGroup = models.ForeignKey(UserGroup, on_delete=models.CASCADE, null=True)
    deleted = models.CharField(max_length=1, default=0)
    inbound = models.ForeignKey(InboundData, on_delete=models.CASCADE, null=True)
    outbound = models.ForeignKey(Outbound, on_delete=models.CASCADE, null=True)
    borrow = models.ForeignKey(Borrow, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=2,choices=status_list, default=0)


class SequencesSequence(models.Model):
    name = models.CharField(primary_key=True, max_length=100)
    last = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'sequences_sequence'

class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'

