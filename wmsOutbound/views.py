from django.shortcuts import render, redirect

# from .forms import *
from WMS.models import *

from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied

from pprint import pprint
import datetime
from WMS.forms import *

from django.db import connection
from django.db import models

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
            'outbound': Outbound.objects.all(),
            'role': request.session['role'],
            'username': request.session['username'],
            'title': 'Outbound | WMS Poltekpos'
        }
        return render(request, "content/main_outbound.html", context)


def outbound(request, id=0):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        if request.session['role'] == "OPR":
            raise PermissionDenied
        else:
            if request.method == "GET":
                if id == 0:
                    form = OutboundForm()
                    date_time = datetime.datetime.now()
                    date_id = date_time.strftime("%d%m%Y%H%M%S")
                    date = date_time.strftime("%Y-%m-%d")
                    id_outbound = date_id
                    con_cre = request.session['id']
                    context = {
                        'form': form,
                        'title': 'Add Outbound',
                        'date': date,
                        'group_id': request.session['usergroup'],
                        'id_outbound': id_outbound,
                        'con_cre': con_cre,
                    }
                    return render(request, 'content/outbound.html', context)
                else:
                    outbound = Outbound.objects.get(pk=id)
                    form = OutboundForm(instance=outbound)
                    date_time = datetime.datetime.now()
                    date = date_time.strftime("%Y-%m-%d")
                    context = {
                        'form': form,
                        'outbound': outbound,
                        'date': date,
                        'group_id': request.session['usergroup'],
                        'title': 'Update Outbound'
                    }
                return render(request, 'content/update_outbound.html', context)
            else:
                if id == 0:
                    form = OutboundForm(request.POST)
                else:
                    outbound = Outbound.objects.get(pk=id)
                    form = OutboundForm(request.POST, instance=outbound)
                if form.is_valid():
                    form.save()
                    return redirect('outbound')
            return render(request, 'content/outbound.html')


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
        outbound = Outbound.objects.filter(pk=id)
        results2 = OutboundData.objects.all().filter(outbound=id)
        request.session['outbound_id'] = id
        context = {
            'Outbound': outbound,
            'Outbounddata': results2,
            'title': 'View outbound',
        }
        return render(request, 'content/view_outbound.html', context)


def outbounddata(request, id=0):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        if request.session['role'] == "OPR":
            raise PermissionDenied
        else:
            if request.method == "GET":
                if id == 0:
                    form = OutboundDataForm()
                    item = Item.objects.all()
                    outboundid = request.session['outbound_id']
                    context = {
                        'form': form,
                        'title': 'Add Outbounddata',
                        'group_id': request.session['usergroup'],
                        'item': item,
                        'outboundid': outboundid,
                    }
                    return render(request, 'content/outbounddata.html', context)
                else:
                    outbounddata = OutboundData.objects.get(pk=id)
                    item = Item.objects.all()
                    form = OutboundDataForm(instance=outbounddata)
                    outboundid = request.session['outbound_id']
                    context = {
                        'title': 'Update Outbounddata',
                        'form': form,
                        'item': item,
                        'outbounddata': outbounddata,
                        'outboundid': outboundid,
                        'group_id': request.session['usergroup'],
                    }
                    return render(request, 'content/update_outbounddata.html', context)
            else:
                if id == 0:
                    form = OutboundDataForm(request.POST)
                else:
                    outbounddata = OutboundData.objects.get(pk=id)
                    form = OutboundDataForm(
                        request.POST, instance=outbounddata)
                if form.is_valid():
                    form.save()
                    return redirect('view_outbound', id=request.session['outbound_id'])
            return render(request, 'content/outbounddata.html')


def delete_outbounddata(request, id):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        if request.session['role'] == "OPR":
            raise PermissionDenied
        else:
            OutboundData.objects.filter(
                pk=id, userGroup=request.session['usergroup']).update(deleted=1)
            return redirect('view_outbound', id=request.session['outbound_id'])

# =========================================== Konfirm ======================================


def confirm(request):
    if '0' not in request.session and '1' not in request.session and '2' not in request.session:
        return redirect('login')
    else:
        role = request.session['2']
        if role == 'OPR':
            raise PermissionDenied
        else:
            outbound_id = request.session['outbound_id']
            Outbound.objects.filter(id=outbound_id).update(status="Ready")
            return redirect('outbound')

# --------------------------- PDF OUTBOUND ------------------------------


class PdfOutbound(View):
    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(Outbound, pk=kwargs['pk'])
        if obj.status == '1':
            raise PermissionDenied
        else:
            datas = list(OutboundData.objects.all().select_related(
                'outbound').filter(outbound=obj).values_list('id', 'item__name', 'quantity', 'outbound'))
            pdf = render_to_pdf('content/pdf_outbound.html',
                                {'datas': datas, 'obj': obj})
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
