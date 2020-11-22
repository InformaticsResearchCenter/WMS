from django import forms
from WMS.models import *
from WMS.models import User, Category, Subcategory

from WMS.models import User, Category
from WMS.models import User, Category


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'role',
            'userGroup',
            'name',
            'address',
            'postalCode',
            'phoneNumber',
        ]


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = [
            'name',
            'subcategory',
            'userGroup',
        ]


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = [
            'category',
            'userGroup',
        ]


class SubcategoryForm(forms.ModelForm):
    class Meta:
        model = Subcategory
        fields = [
            'subcategory',
            'category',
            'userGroup',
        ]


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = [
            'id',
            'name',
            'email',
            'phoneNumber',
            'address',
            'postalCode',
            'userGroup',
        ]
