from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied
import datetime
from WMS.models import *
from WMS.forms import *


def borrowIndex(request):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        context = {
            'role': request.session['role'],
            'username': request.session['username'],
            'title': 'Borrow | Inbound',
            'borrow': Borrow.objects.filter(deleted=0, userGroup=request.session['usergroup'])
        }
        return render(request, 'inside/wmsBorrow/borrowIndex.html', context)


def borrow(request, id=0):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        if request.session['role'] == 'OPR':
            raise PermissionDenied
        else:
            if request.method == "GET":
                if id == 0:
                    context = {
                        'form': BorrowForm(),
                        'id': request.session['id'],
                        'role': request.session['role'],
                        'group_id': request.session['usergroup'],
                        'username': request.session['username'],
                        'title': 'Add Borrow Data',
                    }
                    return render(request, 'inside/wmsBorrow/borrowCreate.html', context)
                else:
                    borrow = Borrow.objects.get(pk=id)
                    context = {
                        'form': BorrowForm(instance=borrow),
                        'item': Item.objects.filter(deleted=0, userGroup=request.session['usergroup']),
                        'borrow': borrow,
                        'borrow_id': request.session['borrow'],
                        'id': request.session['id'],
                        'role': request.session['role'],
                        'group_id': request.session['usergroup'],
                        'username': request.session['username'],
                        'title': 'Update List Borrow Data',
                    }
                    return render(request, 'inside/wmsBorrow/borrowUpdate.html', context)
            else:
                if id == 0:
                    form = BorrowForm(request.POST)
                else:
                    borrow = Borrow.objects.get(pk=id)
                    form = BorrowForm(
                        request.POST, instance=borrow)
                if form.is_valid():
                    form.save()
                    return redirect('borrowIndex')


def borrowDelete(request, id):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        if request.session['role'] == "OPR":
            raise PermissionDenied
        else:
            borrow = Borrow.objects.filter(
                pk=id, userGroup=request.session['usergroup'])
            borrowstatus = borrow.first()
            if borrowstatus.status != '1':
                raise PermissionDenied
            else:
                borrow.update(deleted=1)
                return redirect('borrowIndex')


def borrowView(request, id):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        borrow = Borrow.objects.get(pk=id)
        if borrow.deleted == '0':
            request.session['borrow'] = id
            borrow = BorrowData.objects.filter(
                deleted=0, borrow=id, userGroup=request.session['usergroup'])
            context = {
                'borrowdata': borrow,
                'borrowstatus': borrow.first(),
                'title': 'View Borrow Data',
            }
            return render(request, 'inside/wmsBorrow/borrowView.html', context)
        else:
            raise PermissionDenied


def borrowdata(request, id=0):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        if request.session['role'] == 'OPR':
            raise PermissionDenied
        else:
            if request.method == "GET":
                if id == 0:
                    context = {
                        'form': BorrowdataForm(),
                        'item': Item.objects.filter(deleted=0, userGroup=request.session['usergroup']),
                        'borrow_id': request.session['borrow'],
                        'id': request.session['id'],
                        'role': request.session['role'],
                        'group_id': request.session['usergroup'],
                        'username': request.session['username'],
                        'title': 'Add List Borrow Data',
                    }
                    return render(request, 'inside/wmsBorrow/borrowdataCreate.html', context)
                else:
                    borrowdata = BorrowData.objects.get(pk=id)
                    context = {
                        'form': BorrowdataForm(instance=borrowdata),
                        'item': Item.objects.filter(deleted=0, userGroup=request.session['usergroup']),
                        'borrowdata': borrowdata,
                        'borrow_id': request.session['borrow'],
                        'id': request.session['id'],
                        'role': request.session['role'],
                        'group_id': request.session['usergroup'],
                        'username': request.session['username'],
                        'title': 'Update List Borrow Data',
                    }
                    return render(request, 'inside/wmsBorrow/borrowdataUpdate.html', context)
            else:
                if id == 0:
                    form = BorrowdataForm(request.POST)
                else:
                    borrowdata = BorrowData.objects.get(pk=id)
                    form = BorrowdataForm(
                        request.POST, instance=borrowdata)
                if form.is_valid():
                    form.save()
                    return redirect('borrowView', id=request.session['borrow'])


def borrowdataDelete(request, id):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        if request.session['role'] == "OPR":
            raise PermissionDenied
        else:
            borrowdata = BorrowData.objects.filter(
                pk=id, userGroup=request.session['usergroup'])
            borrowstatus = borrowdata.first()
            if borrowstatus.borrow.status != '1':
                raise PermissionDenied
            else:
                borrowdata.update(deleted=1)
                return redirect('borrowView', id=request.session['borrow'])


def borrowdataConfirm(request):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        if request.session['role'] == 'OPR':
            raise PermissionDenied
        else:
            borrow = Borrow.objects.filter(
                pk=request.session['borrow']).first()
            if borrow.status == '1':
                Borrow.objects.filter(
                    pk=request.session['borrow']).update(status='2', date=datetime.datetime.now())
                return redirect('borrowView', id=request.session['borrow'])
            else:
                raise PermissionDenied


def borrowdataComplete(request):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        if request.session['role'] == 'OPR':
            raise PermissionDenied
        else:
            borrow = Borrow.objects.filter(
                pk=request.session['borrow']).first()
            if borrow.status == '2':
                Borrow.objects.filter(
                    pk=request.session['borrow']).update(status='3')
                return redirect('borrowView', id=request.session['borrow'])
            else:
                raise PermissionDenied


def borrowdataReturn(request):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        if request.session['role'] == 'OPR':
            raise PermissionDenied
        else:
            borrow = Borrow.objects.filter(
                pk=request.session['borrow']).first()
            if borrow.status == '3':
                Borrow.objects.filter(
                    pk=request.session['borrow']).update(status='4')
                return redirect('borrowView', id=request.session['borrow'])
            else:
                raise PermissionDenied
