from django import forms
from WMS.models import *


class RackForm(forms.ModelForm):
    class Meta:
        model = Rack
        fields = [
            'id'
        ]


class BinForm(forms.ModelForm):
    class Meta:
        model = Binlocation
        fields = [
            'id',
            'rackid',
            'capacity'
        ]
