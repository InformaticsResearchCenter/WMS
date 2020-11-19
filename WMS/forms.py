from django import forms
from WMS.models import User, Category


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'password',
            'role',
            'userGroup',
            'name',
            'address',
            'postalCode',
            'phoneNumber',
        ]


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = [
            'id',
            'category',
            'userGroup',
        ]
