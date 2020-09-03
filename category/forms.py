from django import forms
from WMS.models import Category


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = [
            'id',
            'name'
        ]
