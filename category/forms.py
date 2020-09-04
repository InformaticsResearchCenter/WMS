from django import forms
from WMS.models import Category, Subcategory


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
