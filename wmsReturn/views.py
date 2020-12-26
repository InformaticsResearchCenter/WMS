from django.shortcuts import render, redirect
import datetime
from WMS.models import *
from django.core.exceptions import PermissionDenied
from WMS.forms import *
from module import item as it
from django.contrib import messages
from django.db import connection
from sequences import get_next_value, get_last_value
# -------- PDF -----------
from django.template.loader import get_template
from category.utils import render_to_pdf
from django.http import HttpResponse
from django.views.generic import View
from django.shortcuts import get_list_or_404, get_object_or_404
from pprint import pprint
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
                        'id_costumerreturn': get_last_value('costumerreturn_seq'),
                        'date': datetime.datetime.today().strftime('%Y-%m-%d'),
                        'title': 'Add Costumer Return',
                    }
                    return render(request, 'inside/wmsReturn/costumerReturnCreate.html', context)
            else:
                if id == 0:
                    form = CostumerReturnForm(request.POST)
                if form.is_valid():
                    outbound = Outbound.objects.get(
                        pk=request.POST['outbound'])
                    if request.POST['userGroup'] != outbound.userGroup.id:
                        messages.error(request, 'Outbound ID Not exist')
                        return redirect('costumerReturnCreate')
                    form.save()
                    if id == 0:
                        get_next_value('costumerreturn_seq')
                    return redirect('costumerReturnIndex')
                else:
                    messages.error(request, 'Outbound ID Not exist')
                    return redirect('costumerReturnCreate')


def costumerReturnDelete(request, id):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        if request.session['role'] == "OPR":
            raise PermissionDenied
        else:
            costumerReturn = CostumerReturn.objects.filter(
                pk=id, deleted=0, userGroup=request.session['usergroup'])
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
            'costumerReturn': CostumerReturn.objects.filter(pk=id, userGroup=request.session['usergroup'], deleted=0),
            'costumerReturnst': CostumerReturn.objects.filter(pk=id, userGroup=request.session['usergroup'], deleted=0).first().status,
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
                            'id_costumerreturndata': get_last_value('costumerreturndata_seq'),
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
                            'id_costumerreturndata': id
                        }
                        return render(request, 'inside/wmsReturn/costumerReturndataUpdate.html', context)
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
                            if i['item'] == formitem:
                                if i['qty'] < int(formqty):
                                    messages.error(
                                        request, 'Item quantity exceeded the limit !')
                                    return redirect('costumerReturndataCreate')
                                else:
                                    qtyCostumer = list(CostumerReturnData.objects.filter(
                                        costumerReturn=request.session['costumerReturn'], deleted=0).values_list('item__id'))
                                    j = 0
                                    while j < len(qtyCostumer):
                                        if qtyCostumer[j][0] == formitem:
                                            cosRet = CostumerReturnData.objects.filter(
                                                item=i['item'], costumerReturn=request.session['costumerReturn'], userGroup=request.session['usergroup'])
                                            cosRetqty = cosRet.first().quantity
                                            cosRet.update(
                                                quantity=cosRetqty)
                                            return redirect('costumerReturndataIndex', id=request.session['costumerReturn'])
                                        j += 1
                                    form.save()
                                    if id == 0:
                                        get_next_value(
                                            'costumerreturndata_seq')
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
                pk=id, userGroup=request.session['usergroup'], deleted=0)
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
                'costumerReturn').filter(costumerReturn=obj, deleted=0, userGroup=request.session['usergroup']).values_list('id', 'item__name', 'quantity', 'costumerReturn'))
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
        return render(request, 'inside/wmsReturn/return_supplier.html', context)


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
                        'inbound': Inbound.objects.filter(deleted=0, status=2, userGroup=request.session['usergroup']),
                        'form': SupplierReturnForm(),
                        'id': request.session['id'],
                        'role': request.session['role'],
                        'group_id': request.session['usergroup'],
                        'username': request.session['username'],
                        'id_supplierreturn': get_last_value('supplierreturn_seq'),
                        'date': datetime.datetime.today().strftime('%Y-%m-%d'),
                        'title': 'Add Supplier Return',
                    }
                    return render(request, 'inside/wmsReturn/supplierReturnCreate.html', context)
            else:
                if id == 0:
                    form = SupplierReturnForm(request.POST)
                if form.is_valid():
                    form.save()
                    if id == 0:
                        get_next_value('supplierreturn_seq')
                    return redirect('supplierReturnIndex')


def supplierReturnDataIndex(request, id):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        id_inbound = SupplierReturn.objects.filter(
            pk=id, deleted=0, userGroup=request.session['usergroup']).first().inbound.id,
        print(id_inbound[0])
        request.session['id_inbound'] = (id_inbound[0])
        request.session['supplierReturn'] = id
        supplierReturndataStats = SupplierReturnData.objects.filter(
            deleted=0, userGroup=request.session['usergroup'], supplierReturn=id)
        context = {
            'supplierReturn': SupplierReturn.objects.filter(pk=id, deleted=0, userGroup=request.session['usergroup']),
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
                pk=id, userGroup=request.session['usergroup'], deleted=0)
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
                        'inbounddata': InboundData.objects.filter(inbound=request.session['id_inbound'], deleted=0, userGroup=request.session['usergroup']),
                        'supplierReturnId': request.session['supplierReturn'],
                        'id': request.session['id'],
                        'role': request.session['role'],
                        'group_id': request.session['usergroup'],
                        'username': request.session['username'],
                        'date': datetime.datetime.today().strftime('%Y-%m-%d'),
                        'id_supplierreturndata': get_last_value('supplierreturndata_seq'),
                        'title': 'Add Supplier Return Data',
                    }
                    return render(request, 'inside/wmsReturn/supplierReturndataCreate.html', context)
                else:
                    supplierReturn = SupplierReturnData.objects.get(pk=id)
                    context = {
                        'form': SupplierReturndataForm(instance=supplierReturn),
                        'inbounddata': InboundData.objects.filter(inbound=request.session['id_inbound'], deleted=0, userGroup=request.session['usergroup']),
                        'item': it.avaibleItem(1, 0, request.session['usergroup']),
                        'supplierReturnId': request.session['supplierReturn'],
                        'id': request.session['id'],
                        'role': request.session['role'],
                        'group_id': request.session['usergroup'],
                        'username': request.session['username'],
                        'date': datetime.datetime.today().strftime('%Y-%m-%d'),
                        'title': 'Add Supplier Return Data',
                        'supplierreturn': supplierReturn,
                    }
                    return render(request, 'inside/wmsReturn/supplierReturnDataUpdate.html', context)
            else:
                if id == 0:
                    form = SupplierReturndataForm(request.POST)
                else:
                    supplierReturn = SupplierReturnData.objects.get(pk=id)
                    form = SupplierReturndataForm(
                        request.POST, instance=supplierReturn)
                if form.is_valid():
                    formqty = request.POST['quantity']
                    formitem = request.POST['item']
                    rejectCounter = list(InboundData.objects.filter(
                        inbound=request.session['id_inbound'], deleted=0, userGroup=request.session['usergroup']).values('rejectCounter', 'item'))
                    pprint(rejectCounter[0]['rejectCounter'])
                    pprint(rejectCounter)
                    for s in rejectCounter:
                        if formitem == (s['item']):
                            if int(formqty) > (s['rejectCounter']):
                                messages.error(
                                    request, 'Item quantity exceeded the limit !')
                                return redirect('supplierReturndataCreate')
                    item = it.avaibleItem(1, 0, request.session['usergroup'])
                   # for s in rejectCounter:
                    for i in item:
                        if i['item'] == formitem:
                            if int(formqty) > (s['rejectCounter']):
                                messages.error(
                                    request, 'Item quantity exceeded the limit !')
                                return redirect('supplierReturndataCreate')
                            else:
                                qtySupplier = list(SupplierReturnData.objects.filter(
                                    supplierReturn=request.session['supplierReturn'], deleted=0, userGroup=request.session['usergroup']).values_list('item__id'))
                                j = 0
                                while j < len(qtySupplier):
                                    if qtySupplier[j][0] == formitem:
                                        supRet = SupplierReturnData.objects.filter(
                                            item=qtySupplier[j][0], supplierReturn=request.session['supplierReturn'], delete=0, userGroup=request.session['usergroup'])
                                        pprint(supRet)
                                        supRetqty = supRet.first().quantity
                                        supRet.update(
                                            quantity=supRetqty + int(formqty))
                                        inbounddata2 = InboundData.objects.filter(
                                            item=qtySupplier[j][0], inbound=request.session['id_inbound'], deleted=0, userGroup=request.session['usergroup'])
                                        inbounddata3 = inbounddata2.first()
                                        inbounddata2.update(rejectCounter=inbounddata3.rejectCounter - int(
                                            formqty), quantity=inbounddata3.quantity + int(formqty))
                                        return redirect('supplierReturndataIndex', id=request.session['supplierReturn'])
                                    j += 1
                                form.save()
                                inbounddata2 = InboundData.objects.filter(
                                    item=formitem, inbound=request.session['id_inbound'], deleted=0, userGroup=request.session['usergroup'])
                                inbounddata3 = inbounddata2.first()
                                inbounddata2.update(
                                    rejectCounter=inbounddata3.rejectCounter - int(formqty), quantity=inbounddata3.quantity)
                                if id == 0:
                                    get_next_value(
                                        'supplierreturndata_seq')
                                return redirect('supplierReturndataIndex', id=request.session['supplierReturn'])
                else:
                    return HttpResponse('error')


def supplierReturndataDelete(request, id):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        if request.session['role'] == "OPR":
            raise PermissionDenied
        else:
            supplierReturndata = SupplierReturnData.objects.filter(
                pk=id, deleted=0, userGroup=request.session['usergroup'])
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
        if request.session['role'] == "OPR":
            raise PermissionDenied
        else:
            inboundId = SupplierReturn.objects.filter(
                id=request.session['supplierReturn'], userGroup=request.session['usergroup'], deleted=0).values("inbound")[0]["inbound"]
            inboundData = list(InboundData.objects.filter(
                inbound=inboundId, userGroup=request.session['usergroup'], deleted=0).values_list('id', 'item'))
            supplierReturnData = list(SupplierReturnData.objects.filter(
                supplierReturn=request.session['supplierReturn'], userGroup=request.session['usergroup'], deleted=0).values_list('id', 'item'))
            rejectlist = list(InboundData.objects.filter(inbound=inboundId).exclude(
                rejectCounter=0).values_list('rejectCounter', flat=True))
            # Isi field Itemdata
            data = []
            # Looping insert data ke Itemdata
            j = 0
            for i in supplierReturnData:
                for j in inboundData:
                    print(j)
                    # if i[1] == j[1]:
                    #     data.append(ItemData(id='ITD' + str(get_next_value('itemdata_seq')), inbound=InboundData.objects.get(
                    #         pk=j[0]), userGroup=UserGroup.objects.get(pk=request.session['usergroup'])))
                # ItemData.objects.bulk_create(data)
            # Update status Inbound data
            if len(rejectlist) > 0:
                SupplierReturn.objects.filter(
                    id=request.session['supplierReturn'], deleted=0, userGroup=request.session['usergroup']).update(status="2")
            else:
                SupplierReturn.objects.filter(
                    id=request.session['supplierReturn'], deleted=0, userGroup=request.session['usergroup']).update(status="3")
            return redirect('supplierReturnIndex')


class PdfSupplierReturn(View):
    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(SupplierReturn, pk=kwargs['pk'])
        if obj.status == '1':
            raise PermissionDenied
        else:
            datas = list(SupplierReturnData.objects.all().select_related(
                'supplierReturn').filter(supplierReturn=obj, deleted=0, userGroup=request.session['usergroup']).values_list('id', 'item__name', 'quantity'))
            itemdata = []
            for e in datas:
                itemdata.append(list(ItemData.objects.all().select_related(
                    'inbound').select_related('inbound').filter(inbound=e[0]).values_list('id', flat='true')))
            datacollect = zip(datas, itemdata)
            pdf = render_to_pdf('inside/wmsReturn/pdf_returnsupplier.html',
                                {'datas': datas, 'obj': obj, 'itemdata': itemdata, 'datacollect': datacollect})
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
