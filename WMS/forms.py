from django import forms
from WMS.models import *
from WMS.models import User, Category, Subcategory

from WMS.models import User, Category
from WMS.models import User, Category


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
        model = Item
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


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = [
            'id',
            'name',
            'email',
            'phoneNumber',
            'address',
            'postalCode',
            'userGroup',
        ]


class InboundForm(forms.ModelForm):
    class Meta:
        model = Inbound
        fields = [
            'id',
            'date',
            'status',
            'confirm',
            'create',
            'supplier',
            'userGroup',
        ]


class InboundDataForm(forms.ModelForm):
    class Meta:
        model = InboundData
        fields = [
            'id',
            'inbound',
            'item',
            'quantity',
            'reject',
            'rejectCounter',
            'userGroup',
        ]


class RackForm(forms.ModelForm):
    class Meta:
        model = Rack
        fields = [
            'id',
            'userGroup',
        ]

<<<<<<< HEAD
class OutboundForm(forms.ModelForm):
    class Meta:
        model = Outbound
        fields = [
            'id',
            'name',
            'address',
            'phoneNumber',
            'postalCode',
            'date',
            'confirm',
            'create',
            'userGroup',
        ]

class OutboundDataForm(forms.ModelForm):
    class Meta:
        model = OutboundData
        fields = [
            'id',
            'quantity',
            'item',
            'outbound',
            'userGroup',
        ]
        
=======

class BorrowForm(forms.ModelForm):
    class Meta:
        model = Borrow
        fields = [
            'name',
            'phoneNumber',
            'confirm',
            'create',
            'date',
            'userGroup',
        ]


class BorrowdataForm(forms.ModelForm):
    class Meta:
        model = BorrowData
        fields = [
            'quantity',
            'borrow',
            'item',
            'userGroup',
        ]
>>>>>>> 89c8e23d022acc231ca4627b4cd03dd7e39a678e
