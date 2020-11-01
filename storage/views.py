from django.shortcuts import render, redirect

from .forms import *
from WMS.models import *

from django.http import HttpResponseRedirect, JsonResponse
from django.core.exceptions import PermissionDenied

from pprint import pprint

#from sequences import get_next_value, get_last_value, Sequence

from django.db import connection
from django.db import models
from django.db.models import Count
from django.db.models import Max

from datetime import datetime
from json import dumps, loads


# -------- PDF -----------
from django.template.loader import get_template
from category.utils import render_to_pdf
from django.http import HttpResponse
from django.views.generic import View
from django.shortcuts import get_list_or_404, get_object_or_404

# Create your views here.

'''
=========================================================================================
Bagian load scanner || status complete
=========================================================================================
'''

def scanner(request):
    if '0' not in request.session and '1' not in request.session and '2' not in request.session:
        return redirect('login')
    else:
        role = request.session['2']
        if role != 'MAN':
            raise PermissionDenied
        else:
            data = {
                "item": list(Item.objects.all().select_related('subcategoryid').values_list('id', 'name', 'subcategoryid__name'))
            }
            datas = dumps(data)
            return render(request, 'storage/index.html', {"datas": datas})

def index(request):
    data = {
        "item": list(Item.objects.all().select_related('subcategoryid').values_list('id', 'name', 'subcategoryid__name')), "itembatch":list(Itembatch.objects.all().select_related('itemdataid').values_list('binid','id','itemdataid__itemid'))
    }
    datas = dumps(data)
    return render(request, 'storage/index2.html', {"datas": datas})

'''
=========================================================================================
Bagian checking system || status on-progress
=========================================================================================
'''

def checkItem(request):
    itemCode = list(Itembatch.objects.filter(id=request.POST.get('itemCode', None)).select_related('itemdataid').values_list('binid','itemdataid__itemid'))
    return JsonResponse({'itemData': itemCode }, status=200)

def checkOutbound(request):
    outboundid = request.POST.get('outboundId', None)
    print(outboundid)
    customer = list(Outbound.objects.filter(id=str(outboundid)).values_list('customername','address','phonenumber','date','status'))
    items = list(Outbounddata.objects.filter(outboundid=str(outboundid)).values_list('itemid','quantity'))
    print(items)
    print(Outbound.objects.filter(id="16102020231158").values_list('customername','address','phonenumber','date','status'))
    return JsonResponse({'costumer': customer, 'items' : items} ,status=200)

'''
=========================================================================================
Bagian update itembatch Put, Move, Out || status on-progress
=========================================================================================
'''

def put(request):
    if '0' not in request.session and '1' not in request.session and '2' not in request.session:
        return redirect('login')
    else:
        role = request.session['2']
        if role != 'MAN':
            raise PermissionDenied
        else:
            itemCode = loads(request.POST.get('itemCode', None))
            binlocation = request.POST.get('binlocation', None)

            listput = []
            for i in itemCode:
                data = (binlocation, i["code"])
                listput.append(data)

            pprint(listput)

            # cursor = connection.cursor()
            # query = """UPDATE Itembatch
            #             SET binid=%s
            #             WHERE id=%s"""
            # cursor.executemany(query, listput)

            return JsonResponse({'bin': binlocation, 'itemCode': itemCode}, status=200)


def move(request):
    if '0' not in request.session and '1' not in request.session and '2' not in request.session:
        return redirect('login')
    else:
        role = request.session['2']
        if role != 'MAN':
            raise PermissionDenied
        else:
            itemCode = loads(request.POST.get('itemCode', None))
            binlocation = request.POST.get('binlocation', None)

            listmove = []
            for i in itemCode:
                data = (binlocation, i["code"])
                listmove.append(data)

            cursor = connection.cursor()
            query = """UPDATE Itembatch
                        SET binid=%s
                        WHERE id=%s"""
            cursor.executemany(query, listmove)

            return JsonResponse({'bin': binlocation, 'itemCode': itemCode}, status=200)


def out(request):
    if '0' not in request.session and '1' not in request.session and '2' not in request.session:
        return redirect('login')
    else:
        role = request.session['2']
        if role != 'MAN':
            raise PermissionDenied
        else:
            # itemCode = loads(request.POST.get('itemCode', None))
            # binlocation = request.POST.get('binlocation', None)
            OutId = '16102020205558'

            date_time = datetime.now()
            date = date_time.strftime("%Y-%m-%d")

            itemCode = ['1010202007365191ITM3', '1010202007365188ITM3', '1010202007365186ITM3']

            listout = []
            for i in itemCode:
                data = (date, i)
                listout.append(data)

            Outbound.objects.filter(id=OutId).update(status='Done')

            cursor = connection.cursor()
            query = """UPDATE Itembatch
                        SET out=%s
                        WHERE id=%s"""
            cursor.executemany(query, listout)

            return JsonResponse({'bin': OutId, 'itemCode': itemCode}, status=200)

'''
=========================================================================================
Bagian racking || status complete
=========================================================================================
'''
def rack(request, id=0):
    if '0' not in request.session and '1' not in request.session and '2' not in request.session:
        return redirect('login')
    else:
        role = request.session['2']
        if role == 'OPR':
            raise PermissionDenied
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
    if '0' not in request.session and '1' not in request.session and '2' not in request.session:
        return redirect('login')
    else:
        role = request.session['2']
        rack = Rack.objects.annotate(
            numbin=Count('binlocation')).order_by('id')
        context = {
            'rack': rack,
            'role': role,
            'title': 'Rack | WMS Poltekpos'
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

'''
=========================================================================================
Bagian cetak pdf || status complete
=========================================================================================
'''

class PdfRack(View):
    def get(self, request, *args, **kwargs):
        role = request.session['2']
        if role == 'OPR':
            raise PermissionDenied
        else:
            obj = get_object_or_404(Rack, pk=kwargs['pk'])
            datas = list(Binlocation.objects.all().select_related(
                'rackid').filter(rackid=obj).values_list('id', 'rackid__id', 'capacity'))
            pdf = render_to_pdf('content/pdf_rack.html',
                                {'datas': datas, 'obj': obj, 'rack': rack})
            if pdf:
                response = HttpResponse(pdf, content_type='application/pdf')
                filename = "RackInvoice_%s.pdf" % (12341231)
                content = "inline; filename=%s" % (filename)
                download = request.GET.get("download")
                if download:
                    content = "attachment; filename=%s" % (filename)
                response['Content-Disposition'] = content
                return response
            return HttpResponse("Not Found")

'''
=========================================================================================
function yang masih tahap percobaan
=========================================================================================
'''

def getItemBatch(request):
    item = list(Item.objects.all().select_related('subcategoryid').values_list('id', 'name', 'subcategoryid__name')) 
    itembatch = list(Itembatch.objects.all().select_related('itemdataid').values_list('binid','id','itemdataid__itemid'))
    return JsonResponse({'item': item, 'itembatch': itembatch}, status=200)

def testing(request):
    return JsonResponse({'good':'Always'}, status=200)