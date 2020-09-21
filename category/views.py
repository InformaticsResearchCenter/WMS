from django.shortcuts import render, redirect

from .forms import *
from WMS.models import *

from django.http import HttpResponseRedirect

from pprint import pprint

from sequences import get_next_value

from django.db import connection
from django.db import models

from datetime import datetime

# from jointables.models import Item
# Create your views here.

def dummyFun(request):
    model = Itemdata.objects.all().select_related('inboundid').filter(inboundid="10092020230730872946")
    itemdataidlist=[]
    for i in model:
        itemdataidlist.append(i.id)

    Itemdatalist = []
    for e in model:
        
        Itemdatalist.append(Itembatch.objects.all().select_related('itemdataid').filter(itemdataid=e.id))

    pprint(Itemdatalist)
    datalist = []
    for i in Itemdatalist:
        for x in i:
            datalist.append(x.id)
    
    return render(request, 'content/dummy.html', {'datalist':datalist,'itemdataid':itemdataidlist, 'inboundid':"10092020230730872946"})

def main_category(request, id=0):
    # Login Requirements dengan mengecek session
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
        username = request.session['1']
        context = {
            'list_supplier': Supplier.objects.order_by('id'),
            'username': username,
            'title': 'Supplier | WMS Poltekpos'
        }
        return render(request, 'content/list_supplier.html', context)


def supplier(request, id=0):
    if '0' not in request.session and '1' not in request.session and '2' not in request.session:
        return redirect('login')
    else:
        if request.method == "GET":
            if id == 0:
                form = SupplierForm()
                sup_id = get_next_value("supplier_seq")
                username = request.session['1']
                context = {
                    'form': form,
                    'sup_id': sup_id,
                    'username': username,
                    'title': 'Add Supplier'
                }
                return render(request, 'content/supplier.html', context)
            else:
                supplier = Supplier.objects.get(pk=id)
                form = SupplierForm(instance=supplier)
                username = request.session['1']
                context = {
                    'form': form,
                    'supplier': supplier,
                    'username': username,
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
                return redirect('list_supplier')
        return render(request, 'content/supplier.html')


def supplier_delete(request, id):
    supplier = Supplier.objects.get(pk=id)
    supplier.delete()
    return redirect('list_supplier')


def supplier_detail(request, id):
    supplier = Supplier.objects.get(pk=id)
    form = SupplierForm(instance=supplier)
    username = request.session['1']
    context = {
        'form': form,
        'supplier': supplier,
        'username': username,
        'title': 'Detail Supplier'
    }
    return render(request, 'content/detail_supplier.html', context)

# ------------------------- ITEM --------------------


def main_item(request):
    if '0' not in request.session and '1' not in request.session and '2' not in request.session:
        return redirect('login')
    else:
        username = request.session['1']
        cursor = connection.cursor()
        cursor.execute(
            "select item.id, item.name, subcategory.name from item join subcategory on item.subcategoryid=subcategory.id")
        results = cursor.fetchall()
        context = {
            'title': 'Item | WMS Poltekpos',
            'username': username,
            'Item': results
        }
        return render(request, 'content/main_item.html', context)


def item(request, id=0):
    if '0' not in request.session and '1' not in request.session and '2' not in request.session:
        return redirect('login')
    else:
        subcategory = Subcategory.objects.all()
        if request.method == "GET":
            if id == 0:
                form = ItemForm()
                item_id = get_next_value("item_seq")
                username = request.session['1']
                context = {
                    'form': form,
                    'item_id': item_id,
                    'subcategory': subcategory,
                    'title': 'Add Item',
                    'username': username
                }
                return render(request, 'content/item.html', context)
            else:
                item = Item.objects.get(pk=id)
                form = ItemForm(instance=item)
                cursor = connection.cursor()
                cursor.execute(
                    "select item.id, item.name, subcategory.name from item join subcategory on item.subcategoryid=subcategory.id")
                results = cursor.fetchall()
                username = request.session['1']
                context = {
                    'form': form,
                    'item': item,
                    'subcategory': subcategory,
                    'Item': results,
                    'title': 'Update Item',
                    'username': username
                }
                return render(request, 'content/update_item.html', context)
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


# ------------------ Inbound -------------------


def inbound(request, id=0):
    if '0' not in request.session and '1' not in request.session and '2' not in request.session:
        return redirect('login')
    else:
        supplier = Supplier.objects.all()
        if request.method == "GET":
            if id == 0:
                form = InbounddataForm()
                date_time = datetime.now()
                date_id = date_time.strftime("%d%m%Y%H%M%S")
                date = date_time.strftime("%Y-%m-%d")
                id_inbound = date_id
                username = request.session['1']
                con_cre = request.session['0']
                context = {
                    'form': form,
                    'supplier': supplier,
                    'title': 'Add Item',
                    'username': username,
                    'date': date,
                    'id_inbound': id_inbound,
                    'con_cre': con_cre
                }
                return render(request, 'content/inbound.html', context)
            # else:
                # item = Item.objects.get(pk=id)
                # form = ItemForm(instance=item)
                # cursor = connection.cursor()
                # cursor.execute(
                # "select item.id, item.name, subcategory.name from item join subcategory on item.subcategoryid=subcategory.id")
                # results = cursor.fetchall()
                # username = request.session['1']
                # context = {
                # 'form': form,
                # 'item': item,
                # 'subcategory': subcategory,
                # 'Item': results,
                # 'title': 'Update Item',
                # 'username': username
                # }
                # return render(request, 'content/update_item.html', context)
        else:
            if id == 0:
                form = InbounddataForm(request.POST)
            # else:
                # item = Item.objects.get(pk=id)
                # form = ItemForm(request.POST, instance=item)
            if form.is_valid():
                form.save()
                return redirect('inbound')
        return render(request, 'content/inbound.html')


def main_inbound(request):
    if '0' not in request.session and '1' not in request.session and '2' not in request.session:
        return redirect('login')
    else:
        cursor = connection.cursor()
        cursor.execute(
            "select inbounddata.id, supplier.name, inbounddata.status, inbounddata.date from inbounddata join supplier on inbounddata.supplierid=supplier.id")
        results = cursor.fetchall()
        username = request.session['1']
        context = {
            'title': 'Item | WMS Poltekpos',
            'username': username,
            'Inbound': results
        }
        return render(request, 'content/main_inbound.html', context)


def view_inbound(request, id):
    if '0' not in request.session and '1' not in request.session and '2' not in request.session:
        return redirect('login')
    else:
        inbound = Inbounddata.objects.filter(pk=id)
        results2 = Itemdata.objects.all().filter(inboundid=id)
        # cursor2 = connection.cursor()
        # cursor2.execute(
        # "select item.name, itemdata.quantity, itemdata.pass, itemdata.reject from itemdata join item on itemdata.itemid = item.id")
        # results2 = cursor2.fetchall()
        request.session['inbound_id'] = id
        context = {
            'Inbound': inbound,
            'Itemdata': results2,
            'title': 'View Inbound',
        }
        return render(request, 'content/view_inbound.html', context)


def delete_inbound(request, id):
    if '0' not in request.session and '1' not in request.session and '2' not in request.session:
        return redirect('login')
    else:
        inbound = Inbounddata.objects.get(pk=id)
        inbound.delete()
        return redirect('inbound')


def item_data(request, id=0):
    if '0' not in request.session and '1' not in request.session and '2' not in request.session:
        return redirect('login')
    else:
        item = Item.objects.all()
        if request.method == "GET":
            if id == 0:
                form = ItemDataForm()
                itd_id = get_next_value("itemdata_seq")
                inbound_id = request.session['inbound_id']
                username = request.session['1']
                context = {
                    'form': form,
                    'itd_id': itd_id,
                    'item': item,
                    'title': 'Add Item',
                    'username': username,
                    'inbound_id': inbound_id
                }
                return render(request, 'content/itemdata.html', context)
            else:
                itemdata = Itemdata.objects.get(pk=id)
                inboundid = request.session['inbound_id']
                form = ItemDataForm(instance=itemdata)
                username = request.session['1']
                context = {
                    'form': form,
                    'itd': itemdata,
                    'item': item,
                    'title': 'Update ItemData',
                    'username': username,
                    'inboundid': inboundid
                }
                return render(request, 'content/update_itemdata.html', context)
        else:
            if id == 0:
                form = ItemDataForm(request.POST)
            else:
                itemdata = Itemdata.objects.get(pk=id)
                form = ItemDataForm(request.POST, instance=itemdata)
            if form.is_valid():
                form.save()
                return redirect('view_inbound', id=request.session['inbound_id'])
        return render(request, 'content/main_inbound.html')


def delete_itemdata(request, id):
    if '0' not in request.session and '1' not in request.session and '2' not in request.session:
        return redirect('login')
    else:
        itemdata = Itemdata.objects.get(pk=id)
        itemdata.delete()
        return redirect('view_inbound', id=request.session['inbound_id'])


def confirm(request):
    index = 0
    inbound_id = request.session['inbound_id']
    itemdata = Itemdata.objects.all().filter(
        inboundid=inbound_id)
    itemdata_id = list(itemdata.values_list('id', flat=True))
    list_itemdata = list(itemdata.values_list('pass_field', flat=True))
    date_time = datetime.now()
    date = date_time.strftime("%Y-%m-%d")
    data_fix = []
    rackid = "Test "
    entry = date
    out = date
    for i in list_itemdata:
        itemdataid = itemdata_id[index]
        for x in range(i):
            confirm_id = str(get_next_value('confirm_seq'))
            id_batch = inbound_id+confirm_id
            data = (id_batch, rackid, entry, out, itemdataid)
            data_fix.append(data)
        index += 1
    cursor = connection.cursor()
    query = """INSERT INTO Itembatch(id, rackid, entry, out, itemdataid)
                VALUES
                (%s, %s, %s, %s, %s) """
    cursor.executemany(query, data_fix)
    return redirect('inbound')


# ------------------------- Return -----------------------------

def fungsi_return(request):
    itemdata = Itemdata.objects.select_related(
        'inboundid').exclude(reject=0).distinct('inboundid')
    context = {
        'itemdata': itemdata,
        'title': 'Return | WMS Poltekpos'
    }
    return render(request, 'content/return.html', context)


def view_return(request, id):
    inbound = Inbounddata.objects.filter(pk=id)
    results = Itemdata.objects.all().filter(inboundid=id).exclude(reject=0)
    request.session['inbound_id'] = id
    context = {
        'Inbound': inbound,
        'Itemdata': results,
        'title': 'View Return',
    }
    return render(request, 'content/view_return.html', context)


def done(request):
    index = 0
    inbound_id = request.session['inbound_id']
    itemdata = Itemdata.objects.all().filter(
        inboundid=inbound_id).exclude(reject=0)
    itemdata_id = list(itemdata.values_list('id', flat=True))
    list_itemdata = list(itemdata.values_list('reject', flat=True))
    list_itemdata_quantity = list(itemdata.values_list('quantity', flat=True))
    date_time = datetime.now()
    date = date_time.strftime("%Y-%m-%d")
    rackid = "Test "
    entry = date
    out = date
    # -------------------- Looping Data ---------------------
    data_fix = []
    for i in list_itemdata:
        itemdataid = itemdata_id[index]
        for x in range(i):
            confirm_id = str(get_next_value('confirm_seq'))
            id_batch = inbound_id+confirm_id
            data = (id_batch, rackid, entry, out, itemdataid)
            data_fix.append(data)
        index += 1
    cursor = connection.cursor()
    query = """INSERT INTO Itembatch(id, rackid, entry, out, itemdataid)
                VALUES
                (%s, %s, %s, %s, %s) """
    cursor.executemany(query, data_fix)
    # -------------- Insert Data to Returndata ----------------
    inboundidlist = []
    itemidlist = []
    statuslist = []
    datelist = []
    iditemdata = []
    for i in itemdata:
        inboundidlist.append(i.inboundid.id)
        itemidlist.append(i.itemid.id)
        statuslist.append(i.inboundid.status)
        datelist.append(i.inboundid.date)
        iditemdata.append(i.id)

    data_return = []
    con_cre = request.session['0']
    for j in range(len(inboundidlist)):
        return_seq = str(get_next_value('return_seq'))
        return_id = 'RTN'+return_seq
        data2 = (return_id, inboundidlist[j], itemidlist[j],
                 statuslist[j], datelist[j], con_cre, con_cre, iditemdata[j])
        data_return.append(data2)
        # Returndata.objects.create(id=return_id, inboundid=inboundidlist[j], itemid=itemidlist[j],
        #                           status=statuslist[j], date=datelist[j], confirm=request.session['0'], created=request.session['0'])

    query2 = """INSERT INTO Returndata(id, inboundid, itemid, status, date, confirm, created, itemdataid)
                 VALUES
                 (%s, %s, %s, %s, %s, %s, %s, %s) """
    cursor.executemany(query2, data_return)
    # ------------- Update Reject = 0 --------------------
    for k in range(len(list_itemdata_quantity)):
        i = Itemdata.objects.get(id=itemdata_id[k])
        i.pass_field = list_itemdata_quantity[k]
        i.save()
    itemdata.update(reject=0)

    return redirect('return')
