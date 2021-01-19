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
            'postalCode',
            'phoneNumber',
            'address',
            'districts',
            'city',
            'province',
            'village',
        ]


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = [
            'id',
            'name',
            'subcategory',
            'userGroup',
        ]


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = [
            'id',
            'category',
            'userGroup',
        ]


class SubcategoryForm(forms.ModelForm):
    class Meta:
        model = Subcategory
        fields = [
            'id',
            'subcategory',
            'category',
            'userGroup',
            'size',
        ]


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = [
            'id',
            'name',
            'email',
            'address',
            'phoneNumber',
            'postalCode',
            'userGroup',
            'districts',
            'city',
            'province',
            'village',
        ]

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            'id',
            'name',
            'email',
            'address',
            'phoneNumber',
            'postalCode',
            'userGroup',
            'districts',
            'city',
            'province',
            'village',
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
            'rack',
            'userGroup',
        ]


class OutboundForm(forms.ModelForm):
    class Meta:
        model = Outbound
        fields = [
            'id',
            'date',
            'confirm',
            'create',
            'userGroup',
            'customer',
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


class BorrowForm(forms.ModelForm):
    class Meta:
        model = Borrow
        fields = [
            'id',
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
            'id',
            'quantity',
            'borrow',
            'item',
            'userGroup',
        ]


class CostumerReturnForm(forms.ModelForm):
    class Meta:
        model = CostumerReturn
        fields = [
            'id',
            'outbound',
            'date',
            'confirm',
            'create',
            'userGroup',
        ]


class CostumerReturndataForm(forms.ModelForm):
    class Meta:
        model = CostumerReturnData
        fields = [
            'id',
            'quantity',
            'costumerReturn',
            'item',
            'userGroup',
        ]


class SupplierReturnForm(forms.ModelForm):
    class Meta:
        model = SupplierReturn
        fields = [
            'id',
            'inbound',
            'date',
            'confirm',
            'create',
            'status',
            'userGroup',
        ]


class SupplierReturndataForm(forms.ModelForm):
    class Meta:
        model = SupplierReturnData
        fields = [
            'id',
            'quantity',
            'supplierReturn',
            'item',
            'userGroup',
        ]
