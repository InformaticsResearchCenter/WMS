from django.shortcuts import render, redirect
import datetime
from WMS.models import *
from django.core.exceptions import PermissionDenied
from WMS.forms import *
from module import item as it
from django.contrib import messages

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
                                form.save()
                                return redirect('costumerReturndataIndex', id=request.session['costumerReturn'])


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
