from django import forms
<<<<<<< HEAD
<<<<<<< HEAD
from WMS.models import *
=======
from WMS.models import User, Category, Subcategory
>>>>>>> 3d75e840509d729c04323b70b1a17b7606074bcf
=======
from WMS.models import User, Category
>>>>>>> parent of f4c45a4... supplier


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
