from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied
import datetime
from WMS.models import *
from WMS.forms import *
from module import item as it
from sequences import get_next_value, get_last_value
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
        'Item': Item.objects.filter(deleted=0, userGroup=request.session['usergroup']).values('id', 'name', 'size', 'colour', 'subcategory', 'subcategory__subcategory')
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
                        'item_id': get_last_value('item_seq'),
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
                    if id == 0:
                        get_next_value('item_seq')
                    return redirect('itemIndex')


def itemDelete(request, id):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        if request.session['role'] == "OPR":
            raise PermissionDenied
        else:
            Item.objects.filter(
                pk=id, userGroup=request.session['usergroup']).update(deleted=1)
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
                        'category_id': get_last_value('category_seq'),
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


def categoryDelete(request, id):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        if request.session['role'] == "OPR":
            raise PermissionDenied
        else:
            Category.objects.filter(
                pk=id, userGroup=request.session['usergroup']).update(deleted=1)
            Subcategory.objects.filter(
                category = id, userGroup=request.session['usergroup']
            ).update(deleted=1)
            return redirect('categoryIndex')
            # Subcategory.objects.filter(
            #     category
            # )


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
            'subcategory': Subcategory.objects.filter(deleted=0, userGroup=request.session['usergroup'], category=id).values('id', 'subcategory', 'category_id', 'size')
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
                        'subcategory_id': get_last_value('subcategory_seq'),
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
                    if id == 0:
                        get_next_value('subcategory_seq')
                    return redirect('subcategoryIndex', id=request.session['category'])


def subcategoryDelete(request, id):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        if request.session['role'] == "OPR":
            raise PermissionDenied
        else:
            Subcategory.objects.filter(
                pk=id, userGroup=request.session['usergroup']).update(deleted=1)
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
        return render(request, 'inside/wmsInbound/list_supplier.html', context)


def supplier(request, id=0):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        if request.session['role'] == "OPR":
            raise PermissionDenied
        else:
            if request.method == "GET":
                if id == 0:
                    context = {
                        'form': SupplierForm(),
                        'id_supplier': get_last_value('supplier_seq'),
                        'group_id': request.session['usergroup'],
                        'username': request.session['username'],
                        'role': request.session['role'],
                        'title': 'Add Supplier | Inbound'
                    }
                    return render(request, 'inside/wmsInbound/supplier.html', context)
                else:
                    supplier = Supplier.objects.get(pk=id)
                    context = {
                        'form': SupplierForm(instance=supplier),
                        'supplier': supplier,
                        'group_id': request.session['usergroup'],
                        'username': request.session['username'],
                        'role': request.session['role'],
                        'title': 'Update Supplier | Inbound'
                    }
                return render(request, 'inside/wmsInbound/update_supplier.html', context)
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
            return render(request, 'inside/wmsInbound/supplier.html')


def supplier_delete(request, id):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        if request.session['role'] == "OPR":
            raise PermissionDenied
        else:
            Supplier.objects.filter(
                pk=id, userGroup=request.session['usergroup']).update(deleted=1)
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
        return render(request, 'inside/wmsInbound/detail_supplier.html', context)

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
                    context = {
                        'form': InboundForm(),
                        'supplier': Supplier.objects.filter(deleted=0, userGroup=request.session['usergroup']).values('id', 'name'),
                        'title': 'Add Item | Inbound',
                        'group_id': request.session['usergroup'],
                        'username': request.session['username'],
                        'role': request.session['role'],
                        'date': datetime.datetime.now().strftime("%Y-%m-%d"),
                        'id_inbound_date': datetime.datetime.now().strftime("%d%m%Y"),
                        'id_inbound': get_last_value('inbound_seq'),
                        'con_cre': request.session['id'],
                    }
                    return render(request, 'inside/wmsInbound/inbound.html', context)
            else:
                if id == 0:
                    form = InboundForm(request.POST)
                if form.is_valid():
                    form.save()
                    if id == 0:
                        get_next_value('inbound_seq')
                    return redirect('inboundIndex')
            return render(request, 'inside/wmsInbound/inbound.html')


def main_inbound(request):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        context = {
            'inbound': Inbound.objects.filter(deleted=0, userGroup=request.session['usergroup']),
            'username': request.session['username'],
            'role': request.session['role'],
            'title': 'Inbound | WMS Poltekpos'
        }
        return render(request, 'inside/wmsInbound/main_inbound.html', context)


def view_inbound(request, id):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        request.session['inbound_id'] = id
        context = {
            'Inbound': Inbound.objects.filter(pk=id, deleted=0, userGroup=request.session['usergroup']),
            'inboundReturnDataStars': InboundData.objects.filter(deleted=0, userGroup=request.session['usergroup'], inbound=id),
            'Itemdata': InboundData.objects.filter(inbound=id, deleted=0, userGroup=request.session['usergroup']),
            'title': 'View Inbound',
        }
        return render(request, 'inside/wmsInbound/view_inbound.html', context)


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
            item = Item.objects.filter(userGroup=request.session['usergroup'], deleted=0).all() 
            if request.method == "GET":
                if id == 0:
                    context = {
                        'form': InboundDataForm(),
                        'item': item,
                        'username': request.session['username'],
                        'role': request.session['role'],
                        'group_id': request.session['usergroup'],
                        'inbound_id': request.session['inbound_id'],
                        'date': datetime.datetime.now().strftime("%Y-%m-%d"),
                        'id_inbounddata_date': datetime.datetime.now().strftime("%d%m%Y"),
                        'inbounddata_id': get_last_value('inbounddata_seq'),
                        'title': 'Add InboundData | Inbound',
                    }
                    return render(request, 'inside/wmsInbound/inbounddata.html', context)
                else:
                    inbounddata = InboundData.objects.get(pk=id)
                    context = {
                        'form': InboundDataForm(instance=inbounddata),
                        'item': item,
                        'title': 'Update ItemData | Inbound',
                        'username': request.session['username'],
                        'role': request.session['role'],
                        'inboundid': request.session['inbound_id'],
                        'inbounddata': inbounddata,
                    }
                    return render(request, 'inside/wmsInbound/update_inbounddata.html', context)
            else:
                if id == 0:
                    form = InboundDataForm(request.POST)
                else:
                    inbounddata = InboundData.objects.get(pk=id)
                    form = InboundDataForm(request.POST, instance=inbounddata)
                if form.is_valid():
                    formqty = request.POST['quantity']
                    formitem = request.POST['item']
                    formreject = request.POST['reject']
                    Inbounddata = list(InboundData.objects.filter(inbound=request.session['inbound_id'], userGroup=request.session['usergroup'], deleted=0).values_list('item__id', flat=True))
                    if id == 0:
                        for i in Inbounddata:
                            if i == formitem:
                                InData = InboundData.objects.filter(item=i, inbound=request.session['inbound_id'], userGroup=request.session['usergroup'], deleted=0)
                                InData.update(quantity=InData.first().quantity + int(formqty), rejectCounter=InData.first().rejectCounter + int(formreject), reject=InData.first().reject + int(formreject) )
                                return redirect('view_inbound', id=request.session['inbound_id'])
                    form.save()
                    if id == 0:
                        get_next_value('inbounddata_seq')
                    return redirect('view_inbound', id=request.session['inbound_id'])
            return render(request, 'inside/wmsInbound/view_inbound.html')


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
                'inbound').filter(inbound=obj, deleted=0, userGroup=request.session['usergroup']).values_list('id', 'item__name', 'quantity', 'reject', 'item__size', 'item__colour'))
            itemdata = []
            for e in datas:
                itemdata.append(list(ItemData.objects.all().select_related(
                    'inbound').select_related('inbound').filter(inbound=e[0], deleted=0, userGroup=request.session['usergroup']).values_list('id', flat='true')))
                # itemdata.append(list(InboundData.objects.all().select_related(
                #     'item').select_related('item__inbound').filter(inbound=obj).values_list('id', flat='true')))
            datacollect = zip(datas, itemdata)
            ug = UserGroup.objects.get(pk=request.session['usergroup'])
            pdf = render_to_pdf('inside/wmsInbound/pdf_inbound.html', {
                                'datas': datas, 'obj': obj, 'itemdata': itemdata, 'datacollect': datacollect, 'ug': ug,'i':i})
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


# -------------------------- Confirm --------------------------------

def confirm(request):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        if request.session['role'] == "OPR":
            raise PermissionDenied
        else:
            inbounddata_id_list = list(InboundData.objects.filter(inbound=request.session['inbound_id'], deleted=0,userGroup=request.session['usergroup']).values_list('id','quantity', 'rejectCounter'))
            rejectlist = list(InboundData.objects.filter(inbound=request.session['inbound_id'], deleted=0, userGroup=request.session['usergroup']).exclude(rejectCounter=0).values_list('rejectCounter', flat=True))
            print(rejectlist)
            # Isi field Itemdata
            data = []
            #Looping insert data ke Itemdata
            for i in inbounddata_id_list:
                for j in range(i[1] - i[2]):
                    data.append(ItemData(id='ITD'+ str(get_next_value('itemdata_seq')), inbound=InboundData.objects.get(pk=i[0]), userGroup=UserGroup.objects.get(pk=request.session['usergroup'])))
            
            ItemData.objects.bulk_create(data)

            # # --------------------------------------------

            # Update status Inbound data
            if len(rejectlist) > 0:
                Inbound.objects.filter(
                    id=request.session['inbound_id']).update(status="2")
            else:
                Inbound.objects.filter(
                    id=request.session['inbound_id']).update(status="3")
            # # -------------------------------------------------

            return redirect('view_inbound', id=request.session['inbound_id'])
