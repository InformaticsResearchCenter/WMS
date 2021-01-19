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
    context = {
        'role': request.session['role'],
        'username': request.session['username'],
        'title': 'Item | Scanner',
    }
    return render(request, 'inside/wmsStorage/index.html',context)
def getItemData(request):
    avaibleItem = ItemData.objects.select_related('inbound').filter(
            status='1', deleted=0, userGroup=request.session['usergroup']).values('inbound__item')
    rawitem = []
    for i in avaibleItem:
        found = False
        for a in rawitem:
            if i['inbound__item'] == a['item']:
                a['qty'] += 1
                found = True
                break
        if found == False:
            try:
                rawitem.append({'item': i['inbound__item'], 'name': Item.objects.filter(
                    id=i['inbound__item']).values('name')[0]['name'], 'qty': 1})
            except:
                pass
    name=[]
    qty=[]
    for i in rawitem:
        qty.append(i['qty'])
        name.append(i['name'])

    return JsonResponse({'name':name,'qty':qty})

def getStockOpname(request):
    inboundId=request.POST.get('inbound',None)
    inbound = Binlocation.objects.filter(pk=inboundId,deleted=0).values()
    inbounddata = InboundData.objects.filter(inbound=inboundId,deleted=0).values()
    item = []
    for i in inbounddata:
        ref = list(ItemData.objects.filter(inbound=i['id'],deleted=0).values())
        for e in ref:
            item.append(e)
    
    print(inbound)
    print(inbounddata)
    print(item)
    a=0
    for i in item:
        print(i)
        a+=1
    print(a)
    return JsonResponse({"@@":"a"},status = 200)


def getScannerData(request):
    items = list(Item.objects.filter(userGroup = request.session['usergroup'], deleted=0).values('id','name'))
    itemraw1 = list(ItemData.objects.filter(userGroup = request.session['usergroup'], deleted=0, status="1").select_related('inbound').values('id','inbound__item'))
    itemraw2 = list(ItemData.objects.filter(userGroup = request.session['usergroup'], deleted=0, status="0").select_related('inbound').values('id','inbound__item'))
    binlocation = list(Binlocation.objects.select_related('rack').filter(userGroup = request.session['usergroup'], deleted=0, rack__deleted=0).values('id','capacity'))
    itemdata = itemraw1+itemraw2
    item = []
    for i in itemdata:
        for a in items:
            if i['inbound__item'] == a['id']:
                item.append({'id' : i['id'], 'name' : a['name'], 'itemId' : a['id']})
    return JsonResponse({'item': item, 'binlocation' : binlocation, 'itemlist' : items}, status=200)

def getOutboundData(request):
    outbound=request.POST.get('outbound',None)
    print(outbound)
    customer = []
    if outbound != "":
        customer = list(Outbound.objects.filter(id = outbound, userGroup =request.session['usergroup'], deleted=0, status=2).values('id','name','phoneNumber','date'))
        if customer != []:
            item = list(OutboundData.objects.filter(outbound=customer[0]['id']).values('item','quantity'))
            print(item)
            print(customer)
            return JsonResponse({'customer' : customer, 'items' : item}, status = 200)
    return JsonResponse({'msg' : "data not found"}, status=200)
    

def getReturnData(request):
    returnId=request.POST.get('return',None)
    print(returnId)
    customer = []
    if returnId != "":
        customer = list(CostumerReturn.objects.select_related('outbound').filter(id = returnId, userGroup =request.session['usergroup'], deleted=0, status=2).values('id', 'outbound__name', 'outbound__phoneNumber', 'outbound__date'))
        if customer != []:
            item = list(CostumerReturnData.objects.filter(costumerReturn=customer[0]['id']).values('item','quantity'))
            print(item)
            print(customer)
            return JsonResponse({'customer' : customer, 'items' : item}, status = 200)
    return JsonResponse({'msg' : "data not found"}, status=200)

def getBorrowData(request):
    borrowId=request.POST.get('borrow',None)
    employee = []
    if borrowId != "":
        employee = list(Borrow.objects.filter(id = borrowId, userGroup =request.session['usergroup'], deleted=0, status=2).values('id','name','phoneNumber','date'))
        if employee != []:
            item = list(BorrowData.objects.filter(borrow=employee[0]['id']).values('item','quantity'))
            print(item)
            print(employee)
            return JsonResponse({'employee' : employee, 'items' : item}, status = 200)
    return JsonResponse({'msg' : "data not found"}, status=200)
    


def put(request):
    binLocation = request.POST.get('binlocation', None)
    itemCode = loads(request.POST.get('itemCode', None))
    for i in itemCode:
        ItemData.objects.filter(id=i).update(status = "1", binlocation=Binlocation.objects.get(pk=binLocation))
    return JsonResponse({"@@":"a"},status = 200)

def out(request):
    outbound = request.POST.get('outboundId', None)
    itemCode = loads(request.POST.get('itemCode', None))
    for i in itemCode:
        ItemData.objects.filter(id=i).update(status = "2", outbound=Outbound.objects.get(pk=outbound))
    Outbound.objects.filter(id=outbound).update(status = "3")
    return JsonResponse({"@@":"a"},status = 200)

def move(request):
    binLocation = request.POST.get('binlocation', None)
    itemCode = loads(request.POST.get('itemCode', None))
    for i in itemCode:
        ItemData.objects.filter(id=i).update(binlocation=Binlocation.objects.get(pk=binLocation))
    return JsonResponse({"@@":"a"},status = 200)
    
def borrow(request):
    itemCode = loads(request.POST.get('itemCode', None))
    borrowId = request.POST.get('borrowId', None)
    for i in itemCode:
        ItemData.objects.filter(id=i).update(status = "3", borrow=Borrow.objects.get(pk=borrowId))
    Borrow.objects.filter(id=borrowId).update(status = "3")
    return JsonResponse({"@@":"a"},status = 200)

def retur(request):
    itemCode = loads(request.POST.get('itemCode', None))
    returnId = request.POST.get('returnId', None)
    outbound = CostumerReturn.objects.filter(id=returnId).values("outbound__id")
    for i in itemCode:
        ItemData.objects.filter(id=i).update(status = "2", outbound = Outbound.objects.get(pk=outbound[0]["outbound__id"]))
    CostumerReturn.objects.filter(id=returnId).update(status = "3")
    return JsonResponse({"@@":"a"},status = 200)
    
# -------- PDF -----------
from django.template.loader import get_template
from category.utils import render_to_pdf
from django.http import HttpResponse
from django.views.generic import View
from django.shortcuts import get_list_or_404, get_object_or_404
from sequences import get_next_value, get_last_value


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
                    'id': get_last_value('rack_seq'),
                    'title': 'Add Rack',
                }
                return render(request, 'inside/wmsStorage/rackCreate.html', context)
            else:
                form = RackForm(request.POST)
                print('1')
                if form.is_valid():
                    print('2')
                    form.save()
                    numberbin = int(
                        request.POST['row']) * int(request.POST['col'])
                    data_bin = []
                    for i in range(int(numberbin)):
                        binlocation = request.POST['rack']+(str(i+1))
                        data_bin.append(Binlocation(binlocation=binlocation, rack=Rack.objects.get(pk=request.POST['id']),
                                                    capacity=request.POST['capacity'], userGroup=UserGroup.objects.get(pk=request.session['usergroup'])))
                    Binlocation.objects.bulk_create(data_bin)
                    get_next_value('rack_seq')
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


class PdfRack(View):
    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(Rack, pk=kwargs['pk'])
        datas = list(Binlocation.objects.all().select_related(
            'Rack').filter(rack=obj).values_list('binlocation', 'rack__rack', 'capacity'))
        pdf = render_to_pdf('inside/wmsStorage/pdf_rack.html', {
                            'datas': datas, 'obj': obj})
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
