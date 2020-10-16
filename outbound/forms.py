from django import forms
from WMS.models import *


class OutboundForm(forms.ModelForm):
    class Meta:
        model = Outbound
        fields = [
            'id',
            'customername',
            'address',
            'phonenumber',
            'date',
            'status',
        ]

class OutbounddataForm(forms.ModelForm):
	class Meta:
		model = Outbounddata
		fields = [
			'id',
			'itemid',
			'quantity',
			'outboundid',
		]
