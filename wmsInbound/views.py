from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied
import datetime
from WMS.models import *
from WMS.forms import *
from sequences import get_next_value
from WMS.forms import CategoryForm, SubcategoryForm
from django.db import connection
import datetime
# Create your views here.

# -------- PDF -----------
from django.template.loader import get_template
from category.utils import render_to_pdf
from django.http import HttpResponse
from django.views.generic import View
from django.shortcuts import get_list_or_404, get_object_or_404

from WMS.forms import CategoryForm, SubcategoryForm, ItemForm, SupplierForm

# Create your views here.

# ========================= ITEM ================================


def itemIndex(request):
    context = {
        'role': request.session['role'],
        'username': request.session['username'],
        'title': 'Item | Inbound',
        'Item': Item.objects.filter(deleted=0, userGroup=request.session['usergroup']).values('id', 'name', 'subcategory')
    }
    return render(request, 'inside/wmsInbound/itemIndex.html', context)


def item(request, id=0):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        if request.session['role'] == "OPR":
            raise PermissionDenied
        else:
            if request.method == "GET":
                if id == 0:
                    context = {
                        'form': ItemForm(),
                        'subcategory': Subcategory.objects.filter(deleted=0, userGroup=request.session['usergroup']),
                        'group_id': request.session['usergroup'],
                        'role': request.session['role'],
                        'username': request.session['username'],
                        'title': 'Add Item | Inbound'
                    }
                    return render(request, 'inside/wmsInbound/itemCreate.html', context)
                else:
                    item = Item.objects.get(pk=id)
                    context = {
                        'form': ItemForm(instance=item),
                        'item': item,
                        'subcategory': Subcategory.objects.filter(deleted=0, userGroup=request.session['usergroup']),
                        'role': request.session['role'],
                        'group_id': request.session['usergroup'],
                        'username': request.session['username'],
                        'title': 'Update Item | Inbound'
                    }
                    return render(request, 'inside/wmsInbound/itemUpdate.html', context)
            else:
                if id == 0:
                    form = ItemForm(request.POST)
                else:
                    item = Item.objects.get(pk=id)
                    form = ItemForm(request.POST, instance=item)
                if form.is_valid():
                    form.save()
                    return redirect('itemIndex')


def itemDelete(request, id):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        if request.session['role'] == "OPR":
            raise PermissionDenied
        else:
            Item.objects.filter(pk=id, userGroup=request.session['usergroup']).update(deleted=1)
            return redirect('itemIndex')

# ==================== CATEGORY ======================


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
                    return redirect('categoryIndex')


def categoryDelete(request, id):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        if request.session['role'] == "OPR":
            raise PermissionDenied
        else:
            Category.objects.filter(pk=id, userGroup=request.session['usergroup']).update(deleted=1)
            return redirect('categoryIndex')


# ============================= SUBCATEGORY =================================

def subcategoryIndex(request, id):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        request.session['category'] = id
        context = {
            'id': Category.objects.get(pk=id),
            'role': request.session['role'],
            'username': request.session['username'],
            'title': 'Subcategory | Inbound',
            'subcategory': Subcategory.objects.filter(deleted=0, userGroup=request.session['usergroup'], category=id).values('id', 'subcategory', 'category_id')
        }
        return render(request, 'inside/wmsInbound/subcategoryIndex.html', context)


def subcategory(request, id=0):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        if request.session['role'] == "OPR":
            raise PermissionDenied
        else:
            if request.method == "GET":
                if id == 0:
                    context = {
                        'form': SubcategoryForm(),
                        'category': Category.objects.get(pk=request.session['category']),
                        'group_id': request.session['usergroup'],
                        'role': request.session['role'],
                        'username': request.session['username'],
                        'title': 'Add Subcategory | Inbound'
                    }
                    return render(request, 'inside/wmsInbound/subcategoryCreate.html', context)
                else:
                    subcategory = Subcategory.objects.get(pk=id)
                    context = {
                        'form': SubcategoryForm(instance=subcategory),
                        'subcategory': subcategory,
                        'role': request.session['role'],
                        'group_id': request.session['usergroup'],
                        'username': request.session['username'],
                        'title': 'Update Subcategory | Inbound'
                    }
                    return render(request, 'inside/wmsInbound/subcategoryUpdate.html', context)
            else:
                if id == 0:
                    form = SubcategoryForm(request.POST)
                else:
                    subcategory = Subcategory.objects.get(pk=id)
                    form = SubcategoryForm(request.POST, instance=subcategory)
                if form.is_valid():
                    form.save()
                    return redirect('subcategoryIndex', id=request.session['category'])


def subcategoryDelete(request, id):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        if request.session['role'] == "OPR":
            raise PermissionDenied
        else:
            Subcategory.objects.filter(pk=id, userGroup=request.session['usergroup']).update(deleted=1)
            return redirect('subcategoryIndex', id=request.session['category'])


# ------------------------------ SUPLIER -------------------------------------

def list_supplier(request):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        context = {
            'list_supplier': Supplier.objects.filter(deleted=0, userGroup=request.session['usergroup']).values('id', 'name'),
            'username': request.session['username'],
            'role': request.session['role'],
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
                    return redirect('list_supplier')
            return render(request, 'content/supplier.html')


def supplier_delete(request, id):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        if request.session['role'] == "OPR":
            raise PermissionDenied
        else:
            Supplier.objects.filter(pk=id, userGroup=request.session['usergroup']).update(deleted=1)
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

# ======================================= Inbound ============================================

def inbound(request, id=0):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        if request.session['role'] == "OPR":
            raise PermissionDenied
        else:
            if request.method == "GET":
                if id == 0:
                    form = InboundForm()
                    date_time = datetime.datetime.now()
                    date_id = date_time.strftime("%d%m%Y%H%M%S")
                    date = date_time.strftime("%Y-%m-%d")
                    id_inbound = date_id
                    #username = request.session['1']
                    con_cre = request.session['id']
                    context = {
                        'form': form,
                        'supplier': Supplier.objects.filter(deleted=0, userGroup=request.session['usergroup']).values('id', 'name'),
                        'title': 'Add Item',
                        'group_id': request.session['usergroup'],
                        'date': date,
                        'id_inbound': id_inbound,
                        'con_cre': con_cre
                    }
                    return render(request, 'content/inbound.html', context)
            else:
                if id == 0:
                    form = InboundForm(request.POST)
                if form.is_valid():
                    form.save()
                    if id == 0:
                        get_next_value('inbound_seq')
                    return redirect('inboundIndex')    
            return render(request, 'content/inbound.html')


def main_inbound(request):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        context = {
            'inbound': Inbound.objects.filter(deleted=0),
            # 'username': username,
            # 'role': role,
            'title': 'Inbound | WMS Poltekpos'
        }
        return render(request, 'content/main_inbound.html', context)


def view_inbound(request, id):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        inbound = Inbound.objects.filter(pk=id)
        results2 = InboundData.objects.filter(inbound=id, deleted=0)
        request.session['inbound_id'] = id
        context = {
            'Inbound': inbound,
            'Itemdata': results2,
            'title': 'View Inbound',
        }
        return render(request, 'content/view_inbound.html', context)


def delete_inbound(request, id):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        if request.session['role'] == "OPR":
            raise PermissionDenied
        else:
            Inbound.objects.filter(pk=id).update(deleted=1)
            return redirect('inboundIndex')

# ====================================== InboundData ====================================

def inbound_data(request, id=0):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        if request.session['role'] == "OPR":
            raise PermissionDenied
        else:
            item = Item.objects.all()
            if request.method == "GET":
                if id == 0:
                    form = InboundDataForm()
                    context = {
                        'form': form,
                        'item': item,
                        'group_id': request.session['usergroup'],
                        'inbound_id': Inbound.objects.get(pk=request.session['id']),
                        'title': 'Add InboundData',
                    }
                    return render(request, 'content/inbounddata.html', context)
                else:
                    inbounddata = InboundData.objects.get(pk=id)
                    inboundid = request.session['inbound_id']
                    form = InboundDataForm(instance=inbounddata)
                    context = {
                        'form': form,
                        'item': item,
                        'title': 'Update ItemData',
                        'inboundid': inboundid,
                        'inbounddata': inbounddata,
                    }
                    return render(request, 'content/update_inbounddata.html', context)
            else:
                if id == 0:
                    form = InboundDataForm(request.POST)
                else:
                    inbounddata = InboundData.objects.get(pk=id)
                    form = InboundDataForm(request.POST, instance=inbounddata)
                if form.is_valid():
                    form.save()
                    return redirect('view_inbound', id=request.session['inbound_id'])
            return render(request, 'content/view_inbound.html')

def delete_inbounddata(request, id):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        if request.session['role'] == "OPR":
            raise PermissionDenied
        else:
            InboundData.objects.filter(pk=id).update(deleted=1)
            return redirect('view_inbound', id=request.session['inbound_id'])


# -----------------------------PDF ALL Data-------------------------
class PdfInbound(View):
    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(Inbound, pk=kwargs['pk'])
        if obj.status == '1':
            raise PermissionDenied
        else:
            datas = list(InboundData.objects.all().select_related(
                'inbound').filter(inbound=obj).values_list('id', 'item__name', 'quantity', 'rejectCounter', 'reject'))
            itemdata = []
            for e in datas:
                itemdata.append(list(ItemData.objects.all().select_related(
                    'id').filter(id=e[0]).values_list('id', flat='true')))
            datacollect = zip(datas, itemdata)
            pdf = render_to_pdf('content/pdf_inbound.html', {
                                'datas': datas, 'obj': obj, 'itemdata': itemdata, 'datacollect':datacollect})
            if pdf:
                response = HttpResponse(pdf, content_type='application/pdf')
                filename = "Invoice_%s.pdf" % (12341231)
                content = "inline; filename=%s" % (filename)
                download = request.GET.get("download")
                if download:
                    content = "attachment; filename=%s" % (filename)
                response['Content-Disposition'] = content
                return response
            return HttpResponse("Not Found")