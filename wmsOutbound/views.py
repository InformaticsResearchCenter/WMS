from django.shortcuts import render, redirect

# from .forms import *
from WMS.models import *

from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from sequences import get_next_value, get_last_value
from pprint import pprint
import datetime
from WMS.forms import *

from django.db import connection
from django.db import models
from module import item as it

# from datetime import datetime

# -------- PDF -----------
from django.template.loader import get_template
from category.utils import render_to_pdf
from django.http import HttpResponse
from django.views.generic import View
from django.shortcuts import get_list_or_404, get_object_or_404

# ----------------------- Outbound ----------------------


def main_outbound(request):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        context = {
            'outbound': Outbound.objects.filter(deleted=0,userGroup=request.session['usergroup']),
            'role': request.session['role'],
            'username': request.session['username'],
            'title': 'Outbound | WMS Poltekpos'
        }
        return render(request, "inside/wmsOutbound/main_outbound.html", context)


def outbound(request, id=0):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        if request.session['role'] == "OPR":
            raise PermissionDenied
        else:
            if request.method == "GET":
                if id == 0:
                    context = {
                        'form': OutboundForm(),
                        'title': 'Add Outbound | Outbound',
                        'date': datetime.datetime.now().strftime("%Y-%m-%d"),
                        'id_outbound_date': datetime.datetime.now().strftime("%d%m%Y"),
                        'id_outbound': get_last_value('outbound_seq'),
                        'role': request.session['role'],
                        'username': request.session['username'],
                        'group_id': request.session['usergroup'],
                        'con_cre': request.session['id'],
                    }
                    return render(request, 'inside/wmsOutbound/outbound.html', context)
                else:
                    outbound = Outbound.objects.get(pk=id)
                    context = {
                        'form': OutboundForm(instance=outbound),
                        'outbound': outbound,
                        'date': datetime.datetime.now().strftime("%Y-%m-%d"),
                        'group_id': request.session['usergroup'],
                        'role': request.session['role'],
                        'username': request.session['username'],
                        'title': 'Update Outbound | Outbound'
                    }
                return render(request, 'inside/wmsOutbound/update_outbound.html', context)
            else:
                if id == 0:
                    form = OutboundForm(request.POST)
                else:
                    outbound = Outbound.objects.get(pk=id)
                    form = OutboundForm(request.POST, instance=outbound)
                if form.is_valid():
                    form.save()
                    if id == 0:
                        get_next_value('outbound_seq')
                    return redirect('outbound')
            return render(request, 'inside/wmsOutbound/outbound.html')


def delete_outbound(request, id):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        if request.session['role'] == "OPR":
            raise PermissionDenied
        else:
            outbound = Outbound.objects.get(pk=id)
            outbound.delete()
            return redirect('outbound')


def view_outbound(request, id):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        request.session['outbound_id'] = id
        context = {
            'Outbound': Outbound.objects.filter(pk=id,deleted=0,userGroup=request.session['usergroup']),
            'Outboundstats': Outbound.objects.filter(pk=id).first(),
            'Outbounddata': OutboundData.objects.all().filter(outbound=id),
            'Outbounddatastats': OutboundData.objects.all().filter(outbound=id).first(),
            'role': request.session['role'],
            'group_id': request.session['usergroup'],
            'username': request.session['username'],
            'title': 'View outbound',
        }
        return render(request, 'inside/wmsOutbound/view_outbound.html', context)


def outbounddata(request, id=0):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        if request.session['role'] == "OPR":
            raise PermissionDenied
        else:
            if request.method == "GET":
                if id == 0:
                    context = {
                        'form': OutboundDataForm(),
                        'title': 'Add Outbounddata | Outbound',
                        'id_outbounddata': get_last_value('outbounddata_seq'),
                        'role': request.session['role'],
                        'group_id': request.session['usergroup'],
                        'username': request.session['username'],
                        'item': it.avaibleItem(1, 0, request.session['usergroup']),
                        'outboundid': request.session['outbound_id'],
                    }
                    return render(request, 'inside/wmsOutbound/outbounddata.html', context)
                else:
                    outbounddata = OutboundData.objects.get(pk=id)
                    context = {
                        'title': 'Update Outbounddata | Outbound',
                        'form': OutboundDataForm(instance=outbounddata),
                        'item': it.avaibleItem(1, 0, request.session['usergroup']),
                        'outbounddata': outbounddata,
                        'outboundid': request.session['outbound_id'],
                        'group_id': request.session['usergroup'],
                    }
                    return render(request, 'inside/wmsOutbound/update_outbounddata.html', context)
            else:
                if id == 0:
                    form = OutboundDataForm(request.POST)
                else:
                    outbounddata = OutboundData.objects.get(pk=id)
                    form = OutboundDataForm(
                        request.POST, instance=outbounddata)
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
                                return redirect('add_outbounddata')
                            else:
                                qtyOut = list(OutboundData.objects.filter(
                                    outbound=request.session['outbound_id'],deleted=0,userGroup=request.session['usergroup']).values_list('item__id'))
                                j = 0
                                while j < len(qtyOut):
                                    if qtyOut[j][0] == formitem:
                                        out = OutboundData.objects.filter(
                                            item=i['item'], outbound=request.session['outbound_id'], userGroup=request.session['usergroup'])
                                        outqty = out.first().quantity
                                        out.update(
                                            quantity=outqty + int(formqty))
                                        return redirect('view_outbound', id=request.session['outbound_id'])
                                    j += 1
                                form.save()
                                if id == 0:
                                    get_next_value('outbounddata_seq')
                                return redirect('view_outbound', id=request.session['outbound_id'])


def delete_outbounddata(request, id):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        if request.session['role'] == "OPR":
            raise PermissionDenied
        else:
            outstats = OutboundData.objects.filter(
                pk=id, userGroup=request.session['usergroup']).first()
            if outstats.outbound.status == '1':
                OutboundData.objects.filter(
                    pk=id, userGroup=request.session['usergroup']).update(deleted=1)
                return redirect('view_outbound', id=request.session['outbound_id'])
            else:
                raise PermissionDenied

# =========================================== Konfirm ======================================


def confirm(request):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        if request.session['role'] == "OPR":
            raise PermissionDenied
        else:
            outstats = Outbound.objects.filter(
                pk=request.session['outbound_id'], userGroup=request.session['usergroup']).first()
            if outstats.status == '1':
                Outbound.objects.filter(
                    id=request.session['outbound_id']).update(status="2")
                return redirect('view_outbound', id=request.session['outbound_id'])
            else:
                raise PermissionDenied

# --------------------------- PDF OUTBOUND ------------------------------


class PdfOutbound(View):
    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(Outbound, pk=kwargs['pk'])
        if obj.status == '1':
            raise PermissionDenied
        else:
            datas = list(OutboundData.objects.all().select_related(
                'outbound').filter(outbound=obj,deleted=0,userGroup=request.session['usergroup']).values_list('id', 'item__name', 'quantity', 'outbound'))
            pdf = render_to_pdf('inside/wmsOutbound/pdf_outbound.html',
                                {'datas': datas, 'obj': obj})
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
