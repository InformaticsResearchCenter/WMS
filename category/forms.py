from django import forms
from WMS.models import *


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = [
            'id',
            'name'
        ]


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