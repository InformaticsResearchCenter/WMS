from django import forms
from WMS.models import User, Category, Subcategory


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
        model = Category
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
