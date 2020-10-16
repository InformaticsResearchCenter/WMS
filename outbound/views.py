from django.shortcuts import render, redirect

from .forms import *
from WMS.models import *

from django.http import HttpResponseRedirect

from pprint import pprint

from sequences import get_next_value

from django.db import connection
from django.db import models

from datetime import datetime

#-------- PDF -----------
from django.template.loader import get_template
from category.utils import render_to_pdf
from django.http import HttpResponse
from django.views.generic import View
from django.shortcuts import get_list_or_404, get_object_or_404

#----------------------- Outbound ----------------------
def main_outbound(request):
    if '0' not in request.session and '1' not in request.session and '2' not in request.session:
        return redirect('login')
    else:
        context = {'outbound':Outbound.objects.all()}
        return render(request,"content/main_outbound.html", context)


def outbound(request, id=0):
    if '0' not in request.session and '1' not in request.session and '2' not in request.session:
        return redirect('login')
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
            if id == 0:
                form = OutboundForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('outbound')
        return render(request, 'content/outbound.html')

def delete_outbound(request, id):
    if '0' not in request.session and '1' not in request.session and '2' not in request.session:
        return redirect('login')
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
        context = {
            'Outbound': outbound,
            'Outbounddata': results2,
            'title': 'View outbound',
        }
        return render(request, 'content/view_outbound.html', context)

def outbounddata(request, id=0):
    if '0' not in request.session and '1' not in request.session and '2' not in request.session:
        return redirect('login')
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
                pprint(context)
                return render(request, 'content/outbounddata.html', context)
        else:
            if id == 0:
                form = OutbounddataForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('outbound')
        return render(request, 'content/outbounddata.html')

def delete_outbounddata(request, id):
    if '0' not in request.session and '1' not in request.session and '2' not in request.session:
        return redirect('login')
    else:
        outbounddata = Outbounddata.objects.get(pk=id)
        outbounddata.delete()
        return redirect('outbound')

# =========================================== Konfirm =================
def confirm(request):
    outbound_id = request.session['outbound_id']
    Outbound.objects.filter(id=outbound_id).update(status="Complete")
    # Konfirm = Outbound.objects.get(pk=id)
    # Konfirm.status = "Complete"
    # Konfirm.save(update_fields=["status"]) 
    return redirect('outbound')

# --------------------------- PDF OUTBOUND
class PdfOutbound(View):
    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(Outbound, pk=kwargs['pk'])

        datas = list(Outbounddata.objects.all().select_related(
            'outboundid').filter(outboundid=obj).values_list('id', 'itemid__name', 'quantity', 'outboundid'))

        pdf = render_to_pdf('content/pdf_outbound.html',{'datas':datas, 'obj':obj})    
      
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Invoice_%s.pdf" %(12341231)
            content = "inline; filename='%s'" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not Found")            