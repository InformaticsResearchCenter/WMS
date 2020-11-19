from django.shortcuts import render, redirect

# from .forms import *
from WMS.models import *

from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied

from pprint import pprint

from sequences import get_next_value

from django.db import connection
from django.db import models

from datetime import datetime

# -------- PDF -----------
from django.template.loader import get_template
# from category.utils import render_to_pdf
from django.http import HttpResponse
from django.views.generic import View
from django.shortcuts import get_list_or_404, get_object_or_404

# ----------------------- Outbound ----------------------


def main_outbound(request):
    if '0' not in request.session and '1' not in request.session and '2' not in request.session:
        return redirect('login')
    else:
        context = {
            'outbound': Outbound.objects.all(),
            'role': request.session['2'],
            'title': 'Outbound | WMS Poltekpos'
        }
        return render(request, "content/main_outbound.html", context)


def outbound(request, id=0):
    if '0' not in request.session and '1' not in request.session and '2' not in request.session:
        return redirect('login')
    else:
        role = request.session['2']
        if role == 'OPR':
            raise PermissionDenied
        else:
            if request.method == "GET":
                if id == 0:
                    form = OutboundForm()
                    date_time = datetime.now()
                    date_id = date_time.strftime("%d%m%Y%H%M%S")
                    date = date_time.strftime("%Y-%m-%d")
                    id_outbound = date_id
                    context = {
                        'form': form,
                        'title': 'Add Outbound',
                        'date': date,
                        'id_outbound': id_outbound,
                    }
                    return render(request, 'content/outbound.html', context)
                else:
                    outbound = Outbound.objects.get(pk=id)
                    form = OutboundForm(instance=outbound)
                    date_time = datetime.now()
                    date = date_time.strftime("%Y-%m-%d")
                    username = request.session['1']
                    context = {
                        'form': form,
                        'outbound': outbound,
                        'username': username,
                        'date': date,
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
    if '0' not in request.session and '1' not in request.session and '2' not in request.session:
        return redirect('login')
    else:
        role = request.session['2']
        if role == 'OPR':
            raise PermissionDenied
        else:
            outbound = Outbound.objects.get(pk=id)
            outbound.delete()
            return redirect('outbound')


def view_outbound(request, id):
    if '0' not in request.session and '1' not in request.session and '2' not in request.session:
        return redirect('login')
    else:
        outbound = Outbound.objects.filter(pk=id)
        results2 = Outbounddata.objects.all().filter(outboundid=id)
        request.session['outbound_id'] = id
        role = request.session['2']
        context = {
            'Outbound': outbound,
            'role': role,
            'Outbounddata': results2,
            'title': 'View outbound',
        }
        return render(request, 'content/view_outbound.html', context)


def outbounddata(request, id=0):
    if '0' not in request.session and '1' not in request.session and '2' not in request.session:
        return redirect('login')
    else:
        role = request.session['2']
        if role == 'OPR':
            raise PermissionDenied
        else:
            if request.method == "GET":
                if id == 0:
                    form = OutbounddataForm()
                    outbounddata_id = get_next_value("outbounddata_seq")
                    item = Item.objects.all()
                    outboundid = request.session['outbound_id']
                    context = {
                        'form': form,
                        'title': 'Add Outbounddata',
                        'item': item,
                        'outbounddata_id': outbounddata_id,
                        'outboundid': outboundid,
                    }
                    return render(request, 'content/outbounddata.html', context)
                else:
                    outbounddata = Outbounddata.objects.get(pk=id)
                    username = request.session['1']
                    item = Item.objects.all()
                    form = OutbounddataForm(instance=outbounddata)
                    context = {
                        'title': 'Update Outbounddata',
                        'form': form,
                        'username': username,
                        'item': item,
                        'outbounddata': outbounddata
                    }
                    return render(request, 'content/update_outbounddata.html', context)
            else:
                if id == 0:
                    form = OutbounddataForm(request.POST)
                else:
                    outbounddata = Outbounddata.objects.get(pk=id)
                    form = OutbounddataForm(request.POST, instance=outbounddata)
                if form.is_valid():
                    form.save()
                    return redirect('view_outbound', id=request.session['outbound_id'])
            return render(request, 'content/outbounddata.html')


def delete_outbounddata(request, id):
    if '0' not in request.session and '1' not in request.session and '2' not in request.session:
        return redirect('login')
    else:
        role = request.session['2']
        if role == 'OPR':
            raise PermissionDenied
        else:
            outbounddata = Outbounddata.objects.get(pk=id)
            outbounddata.delete()
            return redirect('outbound')

# =========================================== Konfirm =================


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

# --------------------------- PDF OUTBOUND


class PdfOutbound(View):
    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(Outbound, pk=kwargs['pk'])
        if obj.status == 'On - Progress':
            raise PermissionDenied
        else:
            username = request.session['1']
            datas = list(Outbounddata.objects.all().select_related(
                'outboundid').filter(outboundid=obj).values_list('id', 'itemid__name', 'quantity', 'outboundid'))

            pdf = render_to_pdf('content/pdf_outbound.html',
                                {'datas': datas, 'obj': obj, 'username': username})

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
