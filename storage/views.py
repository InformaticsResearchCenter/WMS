from django.shortcuts import render, redirect

from .forms import *
from WMS.models import *

from django.http import HttpResponseRedirect, JsonResponse

from pprint import pprint

from sequences import get_next_value, get_last_value, Sequence

from django.db import connection
from django.db import models
from django.db.models import Count
from django.db.models import Max

from datetime import datetime
from json import dumps


# -------- PDF -----------
from django.template.loader import get_template
from category.utils import render_to_pdf
from django.http import HttpResponse
from django.views.generic import View
from django.shortcuts import get_list_or_404, get_object_or_404

# Create your views here.


def scanner(request):
    data = {
        "item": list(Item.objects.all().select_related('subcategoryid').values_list('id', 'name', 'subcategoryid__name'))
    }
    datas = dumps(data)
    # if request.is_ajax():
    #     text = request.GET.get('data')
    #     return JsonResponse({'Da})
    return render(request, 'storage/index.html', {"datas": datas})


def put(request):
    itemCode = request.POST.get('itemCode', None)
    binlocation = request.POST.get('binlocation', None)
    return JsonResponse({'bin': binlocation, 'itemCode': itemCode}, status=200)

def move(request):
    itemCode = request.POST.get('itemCode', None)
    binlocation = request.POST.get('binlocation', None)
    print(binlocation, itemCode)
    return JsonResponse({'bin': binlocation, 'itemCode': itemCode}, status=200)

def rack(request, id=0):
    if '0' not in request.session and '1' not in request.session and '2' not in request.session:
        return redirect('login')
    else:
        if request.method == "GET":
            if id == 0:
                form = RackForm()
                username = request.session['1']
                context = {
                    'form': form,
                    'title': 'Add Rack',
                    'username': username,
                }
                return render(request, 'storage/rack.html', context)
        else:
            if id == 0:
                form = RackForm(request.POST)
            if form.is_valid():
                form.save()
                cursor = connection.cursor()
                row = request.POST['row']
                col = request.POST['col']
                numberbin = int(row) * int(col)
                rack_id = request.POST['id']
                capacity = request.POST['capacity']
                data_bin = []
                for i in range(int(numberbin)):
                    bin_id = rack_id+(str(i+1))
                    data = (bin_id, rack_id, capacity)
                    data_bin.append(data)

                query = """INSERT INTO Binlocation(id, rackid, capacity)
                 VALUES
                 (%s, %s, %s) """
                cursor.executemany(query, data_bin)
                return redirect('rack')

        return render(request, 'storage/rack.html')


def main_rack(request):
    rack = Rack.objects.annotate(numbin=Count('binlocation')).order_by('id')
    context = {
        'rack': rack,
    }
    return render(request, 'storage/main_rack.html', context)


def view_rack(request, id):
    binlocation = Binlocation.objects.filter(rackid=id)
    max_value = len(binlocation)
    pprint(max_value)
    rack = id
    bin_len = binlocation.count()
    context = {
        'binlocation': binlocation,
        'bin_len': bin_len,
        'rack': rack,
        'title': 'View Rack',
    }
    return render(request, 'storage/view_rack.html', context)


def delete_rack(request, id):
    if '0' not in request.session and '1' not in request.session and '2' not in request.session:
        return redirect('login')
    else:
        rack = Rack.objects.get(pk=id)
        rack.delete()
        return redirect('rack')


# -----------------------------PDF ALL Data Rack-------------------------
class PdfRack(View):
    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(Rack, pk=kwargs['pk'])
        # inbound = Inbounddata.objects.filter(pk=kwargs['pk'])

        datas = list(Binlocation.objects.all().select_related(
            'rackid').filter(rackid=obj).values_list('id', 'rackid__id', 'capacity'))

        # print(datas)
        # print(itembatchs)
        # for data in datas:
        #     print(data[1])
        #     for itembatch in itembatchs:
        #         for item in itembatch:
        #             print(item)

        pdf = render_to_pdf('content/pdf_rack.html',
                            {'datas': datas, 'obj': obj, 'rack': rack})
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Rack_Invoice_%s.pdf" % (12341231)
            content = "inline; filename=%s" % (filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename=%s" % (filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not Found")
