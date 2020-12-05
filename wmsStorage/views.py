from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied
import datetime
from WMS.models import *
from WMS.forms import RackForm
from django.db.models import Count
from django.db.models import Max
from django.http import JsonResponse,HttpResponse
from json import dumps, loads

def scanner(request):
    return render(request, 'inside/wmsStorage/index.html')

def getScannerData(request):
    items = list(Item.objects.filter(userGroup = request.session['usergroup'], deleted=0).values('id','name'))
    itemdata = list(ItemData.objects.filter(userGroup = request.session['usergroup'], deleted=0).select_related('inbound').values('id','inbound__item'))
    binlocation = list(Binlocation.objects.filter(userGroup = request.session['usergroup'], deleted=0).values('id','capacity'))
    item = []
    for i in itemdata:
        for a in items:
            if i['inbound__item'] == a['id']:
                item.append({'id' : i['id'], 'name' : a['name']})
    return JsonResponse({'item': item, 'binlocation' : binlocation}, status=200)

def getOutboundData(request):
    outboundId=request.POST.get('outboundId',None)
    customer = list(Outbound.objects.filter(id = outboundId,userGroup = request.session['usergroup'], deleted=0, status=2).values('id','name','phoneNumber', 'address','postalCode', 'date'))
    if customer != []:
        item = list(OutboundData.objects.filter(outbound=customer[0]['id']).values('item','quantity'))
        return JsonResponse({'customer' : customer, 'items' : item}, status = 200)
    else:
        return JsonResponse({'msg' : "data not found"},status=404)

def getReturnData(request):
    returnId=request.POST.get('return',None)
    customer = list(CostumerReturn.objects.select_related('outbound').filter(id = returnId,userGroup = request.session['usergroup'], deleted=0, status=2).values('id','outbound__name','outbound__phoneNumber', 'outbound__address','outbound__postalCode', 'outbound__date'))
    if customer != []:
        item = list(CostumerReturnData.objects.filter(costumerReturn=customer[0]['id']).values('item','quantity'))
        return JsonResponse({'customer' : customer, 'items' : item}, status = 200)
    else:
        return JsonResponse({'msg' : "data not found"}, status=404)

def getBorrowData(request):
    borrowId=request.POST.get('borrow',None)
    employee = list(Borrow.objects.filter(id = 1,userGroup =1, deleted=0, status=2).values('id','name','phoneNumber','date'))
    if employee != []:
        item = list(BorrowData.objects.filter(borrow=employee[0]['id']).values('item','quantity'))
        return JsonResponse({'employee' : employee, 'items' : item}, status = 200)
    else:
        return JsonResponse({'msg' : "data not found"}, status=404)


def put(request):
    binlocation = request.POST.get('binlocation', None)
    itemCode = loads(request.POST.get('itemCode', None))
    print(binlocation)
    print(itemCode)
    return JsonResponse({"@@":"a"},status = 200)

def out(request):
    return JsonResponse({"@@":"a"},status = 200)

def move(request):
    return JsonResponse({"@@":"a"},status = 200)

def borrow(request):
    return JsonResponse({"@@":"a"},status = 200)

def retur(request):
    return JsonResponse({"@@":"a"},status = 200)

# ===================================== RACK =========================================
def rackIndex(request):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        context = {
            'role': request.session['role'],
            'group_id': request.session['usergroup'],
            'username': request.session['username'],
            'title': 'Rack | Inbound',
            'rack': Rack.objects.filter(deleted=0, userGroup=request.session['usergroup']).annotate(numbin=Count('binlocation')).order_by('id')
        }
        return render(request, 'inside/wmsStorage/rackIndex.html', context)


def rack(request):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        if request.session['role'] == 'OPR':
            raise PermissionDenied
        else:
            if request.method == "GET":
                context = {
                    'form': RackForm(),
                    'role': request.session['role'],
                    'group_id': request.session['usergroup'],
                    'username': request.session['username'],
                    'title': 'Add Rack',
                }
                return render(request, 'inside/wmsStorage/rackCreate.html', context)
            else:
                form = RackForm(request.POST)
                if form.is_valid():
                    form.save()
                    numberbin = int(
                        request.POST['row']) * int(request.POST['col'])
                    data_bin = []
                    for i in range(int(numberbin)):
                        bin_id = request.POST['id']+(str(i+1))
                        data_bin.append(Binlocation(id=bin_id, rack=Rack.objects.get(pk=request.POST['id']),
                                                    capacity=request.POST['capacity'], userGroup=UserGroup.objects.get(pk=request.session['usergroup'])))
                    Binlocation.objects.bulk_create(data_bin)
                    return redirect('rackIndex')

            return render(request, 'inside/wmsStorage/rackIndex.html')


def rackDelete(request, id):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        if request.session['role'] == "OPR":
            raise PermissionDenied
        else:
            Rack.objects.filter(
                pk=id, userGroup=request.session['usergroup']).update(deleted=1)
            Binlocation.objects.filter(
                rack=id, userGroup=request.session['usergroup']).update(deleted=1)
            return redirect('rackIndex')


def rackView(request, id):
    context = {
        'binlocation': Binlocation.objects.filter(rack=id, userGroup=request.session['usergroup']),
        'bin_len': Binlocation.objects.filter(rack=id, userGroup=request.session['usergroup']).count(),
        'rack': id,
        'title': 'View Rack',
    }
    return render(request, 'inside/wmsStorage/rackView.html', context)
