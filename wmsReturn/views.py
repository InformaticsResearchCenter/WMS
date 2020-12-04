from django.shortcuts import render, redirect
import datetime
from WMS.models import *
from django.core.exceptions import PermissionDenied
from WMS.forms import *
from module import item as it
from django.contrib import messages

from django.db import connection

# -------- PDF -----------
from django.template.loader import get_template
from category.utils import render_to_pdf
from django.http import HttpResponse
from django.views.generic import View
from django.shortcuts import get_list_or_404, get_object_or_404
# Create your views here.


def costumerReturnIndex(request):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        context = {
            'costumerReturn': CostumerReturn.objects.filter(deleted=0, userGroup=request.session['usergroup']),
            'role': request.session['role'],
            'username': request.session['username'],
            'title': 'Costumer Return | WMS Poltekpos'
        }
        return render(request, "inside/wmsReturn/costumerReturnIndex.html", context)


def costumerReturn(request, id=0):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        if request.session['role'] == 'OPR':
            raise PermissionDenied
        else:
            if request.method == "GET":
                if id == 0:
                    context = {
                        'form': CostumerReturnForm(),
                        'id': request.session['id'],
                        'role': request.session['role'],
                        'group_id': request.session['usergroup'],
                        'username': request.session['username'],
                        'date': datetime.datetime.today().strftime('%Y-%m-%d'),
                        'title': 'Add Costumer Return',
                    }
                    return render(request, 'inside/wmsReturn/costumerReturnCreate.html', context)
            else:
                if id == 0:
                    form = CostumerReturnForm(request.POST)
                if form.is_valid():
                    form.save()
                    return redirect('costumerReturnIndex')


def costumerReturnDelete(request, id):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        if request.session['role'] == "OPR":
            raise PermissionDenied
        else:
            costumerReturn = CostumerReturn.objects.filter(
                pk=id, userGroup=request.session['usergroup'])
            costumerReturnstatus = costumerReturn.first()
            if costumerReturnstatus.status != '1':
                raise PermissionDenied
            else:
                costumerReturn.update(deleted=1)
                return redirect('costumerReturnIndex')


def costumerReturnDataIndex(request, id):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        request.session['costumerReturn'] = id
        costumerReturndataStats = CostumerReturnData.objects.filter(
            deleted=0, userGroup=request.session['usergroup'], costumerReturn=id)
        context = {
            'costumerReturn': CostumerReturn.objects.filter(pk=id),
            'costumerReturnst': CostumerReturn.objects.filter(pk=id).first().status,
            'costumerReturnData': costumerReturndataStats,
            'costumerReturnDataStats': costumerReturndataStats.first(),
            'role': request.session['role'],
            'username': request.session['username'],
            'title': 'Costumer Return Data | WMS Poltekpos'
        }
        return render(request, "inside/wmsReturn/costumerReturnView.html", context)


def costumerReturndata(request, id=0):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        if request.session['role'] == 'OPR':
            raise PermissionDenied
        else:
            if CostumerReturn.objects.get(pk=request.session['costumerReturn']).status == '1':
                if request.method == "GET":
                    if id == 0:
                        context = {
                            'form': CostumerReturndataForm(),
                            'item': it.avaibleItem(1, 0, request.session['usergroup']),
                            'costumerReturnId': request.session['costumerReturn'],
                            'id': request.session['id'],
                            'role': request.session['role'],
                            'group_id': request.session['usergroup'],
                            'username': request.session['username'],
                            'date': datetime.datetime.today().strftime('%Y-%m-%d'),
                            'title': 'Add Costumer Return Data',
                        }
                        return render(request, 'inside/wmsReturn/costumerReturndataCreate.html', context)
                    else:
                        costumerReturn = CostumerReturn.objects.get(pk=id)
                        context = {
                            'form': CostumerReturndataForm(),
                            'item': it.avaibleItem(1, 0, request.session['usergroup']),
                            'costumerReturnId': request.session['costumerReturn'],
                            'id': request.session['id'],
                            'role': request.session['role'],
                            'group_id': request.session['usergroup'],
                            'username': request.session['username'],
                            'date': datetime.datetime.today().strftime('%Y-%m-%d'),
                            'title': 'Add Costumer Return Data',
                        }
                        return render(request, 'inside/wmsBorrow/borrowUpdate.html', context)
                else:
                    if id == 0:
                        form = CostumerReturndataForm(request.POST)
                    else:
                        costumerReturn = CostumerReturn.objects.get(pk=id)
                        form = CostumerReturndataForm(
                            request.POST, instance=costumerReturn)
                    if form.is_valid():
                        formqty = request.POST['quantity']
                        formitem = request.POST['item']
                        item = it.avaibleItem(
                            1, 0, request.session['usergroup'])
                        for i in item:
                            if i['item'] == int(formitem):
                                if i['qty'] < int(formqty):
                                    messages.error(
                                        request, 'Item quantity exceeded the limit !')
                                    return redirect('costumerReturndataCreate')
                                else:
                                    qtyCostumer = list(CostumerReturnData.objects.filter(
                                        costumerReturn=request.session['costumerReturn']).values_list('item__id'))
                                    j = 0
                                    while j < len(qtyCostumer):
                                        if qtyCostumer[j][0] == int(formitem):
                                            cosRet = CostumerReturnData.objects.filter(
                                                item=i['item'], costumerReturn=request.session['costumerReturn'], userGroup=request.session['usergroup'])
                                            cosRetqty = cosRet.first().quantity
                                            cosRet.update(
                                                quantity=cosRetqty + int(formqty))
                                            return redirect('costumerReturndataIndex', id=request.session['costumerReturn'])
                                        j += 1
                                    form.save()
                                    return redirect('costumerReturndataIndex', id=request.session['costumerReturn'])
            else:
                raise PermissionDenied


def costumerReturndataDelete(request, id):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        if request.session['role'] == "OPR":
            raise PermissionDenied
        else:
            costumerReturndata = CostumerReturnData.objects.filter(
                pk=id, userGroup=request.session['usergroup'])
            costumerReturndatastatus = costumerReturndata.first()
            if costumerReturndatastatus.costumerReturn.status != '1':
                raise PermissionDenied
            else:
                costumerReturndata.update(deleted=1)
                return redirect('costumerReturndataIndex', id=request.session['costumerReturn'])


def costumerReturnConfirm(request):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        if request.session['role'] == 'OPR':
            raise PermissionDenied
        else:
            costumerReturn = CostumerReturn.objects.filter(
                pk=request.session['costumerReturn']).first()
            if costumerReturn.status == '1':
                CostumerReturn.objects.filter(
                    pk=request.session['costumerReturn'], userGroup=request.session['usergroup']).update(status='2')
                return redirect('costumerReturndataIndex', id=request.session['costumerReturn'])
            else:
                raise PermissionDenied


class PdfCostumerReturn(View):
    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(CostumerReturn, pk=kwargs['pk'])
        if obj.status == '1':
            raise PermissionDenied
        else:
            datas = list(CostumerReturnData.objects.all().select_related(
                'costumerReturn').filter(costumerReturn=obj).values_list('id', 'item__name', 'quantity', 'costumerReturn'))
            pdf = render_to_pdf('inside/wmsReturn/pdf_returncostumer.html',
                                {'datas': datas, 'obj': obj})
            if pdf:
                response = HttpResponse(pdf, content_type='application/pdf')
                filename = "CostumerReturnData-%s.pdf" % (12341231)
                content = "inline; filename='%s'" % (filename)
                download = request.GET.get("download")
                if download:
                    content = "attachment; filename='%s'" % (filename)
                response['Content-Disposition'] = content
                return response
            return HttpResponse("Not Found")

# ================================ SUPPLIER Return =============================


def supplierReturnIndex(request):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        context = {
            'username': request.session['username'],
            'title': 'Supplier Return',
            'supplierReturn': SupplierReturn.objects.filter(deleted=0, userGroup=request.session['usergroup']),
        }
        return render(request, 'content/return_supplier.html', context)


def supplierReturn(request, id=0):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        if request.session['role'] == 'OPR':
            raise PermissionDenied
        else:
            if request.method == "GET":
                if id == 0:
                    context = {
                        'inbound': Inbound.objects.filter(deleted=0, status=2),
                        'form': SupplierReturnForm(),
                        'id': request.session['id'],
                        'group_id': request.session['usergroup'],
                        'date': datetime.datetime.today().strftime('%Y-%m-%d'),
                        'title': 'Add Supplier Return',
                    }
                    return render(request, 'inside/wmsReturn/supplierReturnCreate.html', context)
            else:
                if id == 0:
                    form = SupplierReturnForm(request.POST)
                if form.is_valid():
                    form.save()
                    return redirect('supplierReturnIndex')


def supplierReturnDataIndex(request, id):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        id_inbound = SupplierReturn.objects.filter(pk=id).first().inbound.id,
        print(id_inbound[0])
        request.session['id_inbound'] = (id_inbound[0])
        request.session['supplierReturn'] = id
        supplierReturndataStats = SupplierReturnData.objects.filter(
            deleted=0, userGroup=request.session['usergroup'], supplierReturn=id)
        context = {
            'supplierReturn': SupplierReturn.objects.filter(pk=id),
            'supplierReturnData': supplierReturndataStats,
            'supplierReturnDataStats': supplierReturndataStats.first(),
            'role': request.session['role'],
            'username': request.session['username'],
            'title': 'Supplier Return Data | WMS Poltekpos'
        }
        return render(request, "inside/wmsReturn/supplierReturnView.html", context)


def supplierReturnDelete(request, id):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        if request.session['role'] == "OPR":
            raise PermissionDenied
        else:
            supplierReturn = SupplierReturn.objects.filter(
                pk=id, userGroup=request.session['usergroup'])
            supplierReturnstatus = supplierReturn.first()
            if supplierReturnstatus.status != '1':
                raise PermissionDenied
            else:
                supplierReturn.update(deleted=1)
                return redirect('supplierReturnIndex')


def supplierReturndata(request, id=0):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        if request.session['role'] == 'OPR':
            raise PermissionDenied
        else:
            if request.method == "GET":
                if id == 0:
                    context = {
                        'form': SupplierReturndataForm(),
                        'inbounddata': InboundData.objects.filter(inbound=request.session['id_inbound'], deleted=0),
                        'supplierReturnId': request.session['supplierReturn'],
                        'id': request.session['id'],
                        'role': request.session['role'],
                        'group_id': request.session['usergroup'],
                        'username': request.session['username'],
                        'date': datetime.datetime.today().strftime('%Y-%m-%d'),
                        'title': 'Add Supplier Return Data',
                    }
                    return render(request, 'inside/wmsReturn/supplierReturndataCreate.html', context)
                else:
                    supplierReturn = SupplierReturn.objects.get(pk=id)
                    context = {
                        'form': SupplierReturndataForm(),
                        'item': it.avaibleItem(1, 0, request.session['usergroup']),
                        'supplierReturnId': request.session['supplierReturn'],
                        'id': request.session['id'],
                        'role': request.session['role'],
                        'group_id': request.session['usergroup'],
                        'username': request.session['username'],
                        'date': datetime.datetime.today().strftime('%Y-%m-%d'),
                        'title': 'Add Supplier Return Data',
                    }
                    return render(request, 'inside/wmsBorrow/borrowUpdate.html', context)
            else:
                if id == 0:
                    form = SupplierReturndataForm(request.POST)
                else:
                    supplierReturn = SupplierReturn.objects.get(pk=id)
                    form = SupplierReturndataForm(
                        request.POST, instance=supplierReturn)
                if form.is_valid():
                    formqty = request.POST['quantity']
                    formitem = request.POST['item']
                    rejectCounter = list(InboundData.objects.filter(id=request.session['id_inbound']).values('rejectCounter'))
                    if(int(formqty) > rejectCounter[0]['rejectCounter']):
                        messages.error(
                            request, 'Item quantity exceeded the limit !')
                        return redirect('supplierReturndataCreate')
                    else:
                        form.save()
                        return redirect('supplierReturndataIndex', id=request.session['supplierReturn'])
                

def supplierReturndataDelete(request, id):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        if request.session['role'] == "OPR":
            raise PermissionDenied
        else:
            supplierReturndata = SupplierReturnData.objects.filter(
                pk=id, userGroup=request.session['usergroup'])
            supplierReturndatastatus = supplierReturndata.first()
            if supplierReturndatastatus.supplierReturn.status != '1':
                raise PermissionDenied
            else:
                supplierReturndata.update(deleted=1)
                return redirect('supplierReturndataIndex', id=request.session['supplierReturn'])


def supplierReturnConfirm(request):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        if request.session['role'] == 'OPR':
            raise PermissionDenied
        else:
            index = 0
            supplierReturn_id = request.session['supplierReturn']
            inbounddata = InboundData.objects.all().filter(inbound=supplierReturn_id)
            inbounddata_id_list = list(inbounddata.values_list('id', flat=True))
            item_id_list = list(inbounddata.values_list('item', flat=True))
            quantity_list = list(
                inbounddata.values_list('quantity', flat=True))
            print(quantity_list)   

            # Memanggil value RejectCounter yang lebih dari 0
            inbounddata2 = InboundData.objects.all().filter(
                inbound=supplierReturn_id).exclude(rejectCounter=0)
            rejectCounterlist = list(inbounddata2.values_list('rejectCounter', flat=True))

            # Isi field Itemdata
            data_fix = []
            binlocation = None
            userGroup = request.session['usergroup']
            inbound  = None
            outbound = None
            borrow = None
            status = None

            # Looping insert data ke ItemData
            for i in quantity_list:
                #itemid = item_id_list[index]
                inbounddataid = inbounddata_id_list[index]
                for x in range(i):
                    data = (binlocation, userGroup, inbound, outbound, borrow, status)
                    data_fix.append(data)
                index += 1
            cursor = connection.cursor()
            query = """INSERT INTO ItemData(binlocation, userGroup, inbound, outbound, borrow, status)
                        VALUES
                        (%s, %s, %s, %s, %s, %s) """
            cursor.executemany(query, data_fix)
            #--------------------------------------------

            # Update status Inbound data
            if len(rejectCounterlist) > 0:
                Inbound.objects.filter(
                    id=supplierReturn_id).update(status="2")
            else:
                Inbound.objects.filter(id=supplierReturn_id).update(status="3")

            # -----------------------------------------------
            return redirect('supplierReturnIndex')                                 



class PdfSupplierReturn(View):
    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(SupplierReturn, pk=kwargs['pk'])
        if obj.status == '1':
            raise PermissionDenied
        else:
            datas = list(SupplierReturnData.objects.all().select_related(
                'supplierReturn').filter(supplierReturn=obj).values_list('id', 'item__name', 'quantity', 'reject'))
            itemdata = []
            for e in datas:
                itemdata.append(list(ItemData.objects.all().select_related(
                    'id').filter(id=e[0]).values_list('id', flat='true')))
            datacollect = zip(datas, itemdata)
            pdf = render_to_pdf('inside/wmsReturn/pdf_returnsupplier.html',
                                {'datas': datas, 'obj': obj,'itemdata': itemdata, 'datacollect':datacollect})
            if pdf:
                response = HttpResponse(pdf, content_type='application/pdf')
                filename = "Invoice_%s.pdf" % (12341231)
                content = "inline; filename='%s'" % (filename)
                download = request.GET.get("download")
                if download:
                    content = "attachment; filename='%s'" % (filename)
                response['Content-Disposition'] = content
                return response
            return HttpResponse("Not Found")
