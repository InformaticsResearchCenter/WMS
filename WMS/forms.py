from django import forms
from WMS.models import *

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