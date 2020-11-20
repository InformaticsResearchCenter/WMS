from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied
import datetime
from WMS.models import *
from WMS.forms import *
from sequences import get_next_value

from django.db import connection
# Create your views here.


def itemIndex(request):
    return render(request, 'inside/wmsInbound/itemIndex.html')


def categoryIndex(request):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        context = {
            'role': request.session['role'],
            'username': request.session['username'],
            'title': 'Category | Inbound',
            'category': Category.objects.filter(deleted=0, userGroup=request.session['usergroup']).values('id', 'category')
        }
        return render(request, 'inside/wmsInbound/categoryIndex.html', context)


def category(request, id=0):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        if request.session['role'] == "OPR":
            raise PermissionDenied
        else:
            if request.method == "GET":
                if id == 0:
                    context = {
                        'form': CategoryForm(),
                        'id': get_last_value('category_seq'),
                        'group_id': request.session['usergroup'],
                        'role': request.session['role'],
                        'username': request.session['username'],
                        'title': 'Add Category | Inbound'
                    }
                    return render(request, 'inside/wmsInbound/categoryCreate.html', context)
                else:
                    category = Category.objects.get(pk=id)
                    context = {
                        'form': CategoryForm(instance=category),
                        'category': category,
                        'role': request.session['role'],
                        'group_id': request.session['usergroup'],
                        'username': request.session['username'],
                        'title': 'Update Category | Inbound'
                    }
                    return render(request, 'inside/wmsInbound/categoryUpdate.html', context)
            else:
                if id == 0:
                    form = CategoryForm(request.POST)
                else:
                    category = Category.objects.get(pk=id)
                    form = CategoryForm(request.POST, instance=category)
                if form.is_valid():
                    form.save()
                    if id == 0:
                        get_next_value('category_seq')
                    return redirect('categoryIndex')


def category_delete(request, id):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        if request.session['role'] == "OPR":
            raise PermissionDenied
        else:
            Category.objects.filter(pk=id).update(deleted=1)
            return redirect('categoryIndex')


# ------------------------------ SUPLIER -------------------

def list_supplier(request):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        context = {
            'list_supplier': Supplier.objects.filter(deleted=0, userGroup=request.session['usergroup']).values('id', 'name'),
            # 'username': username,
            # 'role': role,
            'title': 'Supplier | WMS Poltekpos'
        }
        return render(request, 'content/list_supplier.html', context)

def supplier(request, id=0):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        if request.session['role'] == "OPR":
            raise PermissionDenied
        else:
            if request.method == "GET":
                if id == 0:
                    form = SupplierForm()
                    #username = request.session['1']
                    context = {
                        'form': form,
                        'id': get_next_value('supplier_seq'),
                        'group_id': request.session['usergroup'],
                        'title': 'Add Supplier'
                    }
                    return render(request, 'content/supplier.html', context)
                else:
                    supplier = Supplier.objects.get(pk=id)
                    form = SupplierForm(instance=supplier)
                    context = {
                        'form': form,
                        'supplier': supplier,
                        'group_id': request.session['usergroup'],
                        'title': 'Update Suppliers'
                    }
                return render(request, 'content/update_supplier.html', context)
            else:
                if id == 0:
                    form = SupplierForm(request.POST)
                else:
                    supplier = Supplier.objects.get(pk=id)
                    form = SupplierForm(request.POST, instance=supplier)
                if form.is_valid():
                    form.save()
                    if id == 0:
                        get_next_value('supplier_seq')
                    return redirect('list_supplier')
            return render(request, 'content/supplier.html')
                    
def supplier_delete(request, id):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        if request.session['role'] == "OPR":
            raise PermissionDenied
        else:
            Supplier.objects.filter(pk=id).update(deleted=1)
            return redirect('list_supplier')


def supplier_detail(request, id):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        supplier = Supplier.objects.get(pk=id)
        form = SupplierForm(instance=supplier)
        context = {
            'form': form,
            'supplier': supplier,
            'title': 'Detail Supplier'
        }
        return render(request, 'content/detail_supplier.html', context)

