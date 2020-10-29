from django import forms
from WMS.models import *


# ------------------- Category -----------------

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = [
            'id',
            'name'
        ]


# ------------------- Subcategory -----------------


class SubcategoryForm(forms.ModelForm):
    class Meta:
        model = Subcategory
        fields = [
            'id',
            'name',
            'categoryid'
        ]

# ---------------------- Supplier ------------


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = [
            'id',
            'name',
            'email',
            'phone',
            'address',
            'postalcode'
        ]

# ---------------------- Item ------------


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = [
            'id',
            'name',
            'subcategoryid'
        ]


# ---------------------- Itemdata ------------


class ItemDataForm(forms.ModelForm):
    class Meta:
        model = Itemdata
        fields = [
            'id',
            'inboundid',
            'itemid',
            'quantity',
            'pass_field',
            'reject',
        ]


# ---------------------- Inbound ------------

class InbounddataForm(forms.ModelForm):
    class Meta:
        model = Inbounddata
        fields = [
            'id',
            'supplierid',
            'status',
            'date',
            'confirm',
            'created',
        ]
# --------------------- Userdata ------------

class UserdataForm(forms.ModelForm):
    class Meta:
        model = Userdata
        fields = [
            'id',
            'username',
            'password',
            'roleid',
            'name',
            'address',
            'phonenumber',
            'email',
        ]