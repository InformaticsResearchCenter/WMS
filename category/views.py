from django.shortcuts import render, redirect

from .forms import *
from WMS.models import *

from django.http import HttpResponseRedirect

from pprint import pprint

from sequences import get_next_value

from django.db import connection
# from jointables.models import Item
# Create your views here.


def main_category(request, id=0):
    if '0' not in request.session and '1' not in request.session and '2' not in request.session:
        return redirect('login')
    else:
        if request.method == "GET":
            if id == 0:
                username = request.session['1']
                form = CategoryForm()
                cat_id = get_next_value("category_seq")
                context = {
                    'title': 'Add Category',
                    'form': form,
                    'username': username,
                    'cat_id': cat_id
                }
                return render(request, 'content/category.html', context)
            else:
                category = Category.objects.get(pk=id)
                username = request.session['1']
                form = CategoryForm(instance=category)
                context = {
                    'title': 'Update Category',
                    'form': form,
                    'username': username,
                    'category': category
                }
                return render(request, 'content/update_category.html', context)
        else:
            if id == 0:
                form = CategoryForm(request.POST)
            else:
                category = Category.objects.get(pk=id)
                form = CategoryForm(request.POST, instance=category)
            if form.is_valid():
                form.save()
                return redirect('list_category')
        return render(request, 'content/category.html')


def list_category(request):
    if '0' not in request.session and '1' not in request.session and '2' not in request.session:
        return redirect('login')
    else:
        category = Category.objects.order_by('id')
        username = request.session['1']
        context = {
            'title': 'List Category',
            'category': category,
            'username': username,
        }
        return render(request, 'content/list_category.html', context)


def delete_category(request, id):
    if '0' not in request.session and '1' not in request.session and '2' not in request.session:
        return redirect('login')
    else:
        category = Category.objects.get(pk=id)
        category.delete()
        return redirect('list_category')


def delete_subcategory(request, id):
    if '0' not in request.session and '1' not in request.session and '2' not in request.session:
        return redirect('login')
    else:
        subcategory = Subcategory.objects.get(pk=id)
        subcategory.delete()
        cat_id = request.session['cat_id']
        return redirect('view_category', id=cat_id)


def main_item(request):
    if '0' not in request.session and '1' not in request.session and '2' not in request.session:
        return redirect('login')
    else:
        username = request.session['1']
        context = {
            'title': 'Item | WMS Poltekpos',
            'username': username
        }
        return render(request, 'content/main_item.html', context)


def view_category(request, id):
    if '0' not in request.session and '1' not in request.session and '2' not in request.session:
        return redirect('login')
    else:
        subcategory = Subcategory.objects.all().filter(categoryid=id)
        category = Category.objects.get(pk=id)
        cat_name = category.name
        request.session['cat_id'] = id
        cat_id = request.session['cat_id']
        username = request.session['1']
        context = {
            'title': 'View Category - Subcategory',
            'subcategory': subcategory,
            'cat_id': cat_id,
            'cat_name': cat_name,
            'username': username,
        }
        return render(request, 'content/view_category.html', context)


def main_subcategory(request, id=0):
    if '0' not in request.session and '1' not in request.session and '2' not in request.session:
        return redirect('login')
    else:
        if request.method == "GET":
            if id == 0:
                username = request.session['1']
                form = SubcategoryForm()
                subcat_id = get_next_value("subcategory_seq")
                cat_id = request.session['cat_id']
                context = {
                    'title': 'Add Subcategory',
                    'form': form,
                    'subcat_id': subcat_id,
                    'username': username,
                    'cat_id': cat_id
                }
                return render(request, 'content/subcategory.html', context)
            else:
                username = request.session['1']
                subcategory = Subcategory.objects.get(pk=id)
                str_subcat_id = str(subcategory.categoryid)
                subcat_id = str_subcat_id[17:-1]
                form = SubcategoryForm(instance=subcategory)
                context = {
                    'title': 'Update Subcategory',
                    'subcategory': subcategory,
                    'subcat_id': subcat_id,
                    'username': username,
                    'form': form
                }
                return render(request, 'content/update_subcategory.html', context)
        else:
            if id == 0:
                form = SubcategoryForm(request.POST)
            else:
                subcategory = Subcategory.objects.get(pk=id)
                form = SubcategoryForm(request.POST, instance=subcategory)
            if form.is_valid():
                cat_id = request.session['cat_id']
                form.save()
                return redirect('view_category', id=cat_id)
        return render(request, 'content/subcategory.html')



# ------------------------------ SUPLIER ------------------- 

def list_supplier(request):
    if '0' not in request.session and '1' not in request.session and '2' not in request.session:
        return redirect('login')
    else:
        context = {'list_supplier':Supplier.objects.order_by('id')}
        return render(request, 'content/list_supplier.html', context)

def supplier(request, id=0):
    if '0' not in request.session and '1' not in request.session and '2' not in request.session:
        return redirect('login')
    else:
        if request.method == "GET":
            if id == 0:
                form = SupplierForm()
                sup_id = get_next_value("supplier_seq")
                return render(request, 'content/supplier.html', {'form': form, 'sup_id': sup_id})
            else:
                supplier = Supplier.objects.get(pk=id)
                form = SupplierForm(instance=supplier)
            return render(request, 'content/update_supplier.html', {'form': form, 'supplier': supplier})   
        else:
            if id == 0:
                form = SupplierForm(request.POST)
            else:
                supplier = Supplier.objects.get(pk=id)
                form = SupplierForm(request.POST, instance=supplier)
            if form.is_valid():
                form.save()
                return redirect('list_supplier')
        return render(request, 'content/supplier.html')   

def supplier_delete(request, id):
    supplier = Supplier.objects.get(pk=id)
    supplier.delete()
    return redirect('list_supplier')

def supplier_detail(request, id):
    supplier = Supplier.objects.get(pk=id)
    form = SupplierForm(instance=supplier)
    return render(request, 'content/detail_supplier.html', {'form': form, 'supplier': supplier})    

# ------------------------- ITEM --------------------
def main_item(request):
    if '0' not in request.session and '1' not in request.session and '2' not in request.session:
        return redirect('login')
    else:
        cursor=connection.cursor()
        cursor.execute("select item.id, item.name, subcategory.name from item join subcategory on item.subcategoryid=subcategory.id")
        results=cursor.fetchall()
        return render(request, 'content/main_item.html', {'Item':results})

def item(request, id=0):
    if '0' not in request.session and '1' not in request.session and '2' not in request.session:
        return redirect('login')
    else:
        subcategory = Subcategory.objects.all()
        if request.method == "GET":
            if id == 0:
                form = ItemForm()
                item_id = get_next_value("item_seq")
                return render(request, 'content/item.html', {'form': form, 'item_id': item_id, 'subcategory': subcategory})
            else:
                item = Item.objects.get(pk=id)
                form = ItemForm(instance=item)
                cursor=connection.cursor()
                cursor.execute("select item.id, item.name, subcategory.name from item join subcategory on item.subcategoryid=subcategory.id")
                results=cursor.fetchall()
                return render(request, 'content/update_item.html', {'form': form, 'item': item, 'subcategory': subcategory, 'Item':results})
        else:
            if id == 0:
                form = ItemForm(request.POST)
            else:
                item = Item.objects.get(pk=id)
                form = ItemForm(request.POST, instance=item)
            if form.is_valid():
                form.save()
                return redirect('item')
        return render(request, 'content/item.html')

def delete_item(request, id):
    if '0' not in request.session and '1' not in request.session and '2' not in request.session:
        return redirect('login')
    else:
        item = Item.objects.get(pk=id)
        item.delete()
        return redirect('item')   