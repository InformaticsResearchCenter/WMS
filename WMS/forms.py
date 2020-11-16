from django import forms
from WMS.models import User

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
