from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied
import datetime
from WMS.models import *
from WMS.forms import *
from module import item as it
from django.contrib import messages
from sequences import get_next_value, get_last_value

# -------- PDF -----------
from django.template.loader import get_template
from category.utils import render_to_pdf
from django.http import HttpResponse
from django.views.generic import View
from django.shortcuts import get_list_or_404, get_object_or_404


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
                        'id_borrow': get_last_value('borrow_seq'),
                        'date': datetime.datetime.today().strftime('%Y-%m-%d'),
                        'title': 'Add Borrow Data',
                    }
                    return render(request, 'inside/wmsBorrow/borrowCreate.html', context)
                else:
                    borrow = Borrow.objects.get(pk=id)
                    context = {
                        'form': BorrowForm(instance=borrow),
                        'item': Item.objects.filter(deleted=0, userGroup=request.session['usergroup']),
                        'borrow': borrow,
                        'borrow_date': datetime.datetime.today().strftime('%Y-%m-%d'),
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
                    if id == 0:
                        get_next_value('borrow_seq')
                    return redirect('borrowIndex')


def borrowDelete(request, id):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        if request.session['role'] == "OPR":
            raise PermissionDenied
        else:
            borrow = Borrow.objects.filter(
                pk=id, userGroup=request.session['usergroup'], deleted=0)
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
            borrowstatus = Borrow.objects.get(pk=id)
            context = {
                'borrowdata': borrow,
                'borrowstats': borrowstatus,
                'borrowstatus': borrow.first(),
                'role': request.session['role'],
                'group_id': request.session['usergroup'],
                'username': request.session['username'],
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
            if Borrow.objects.get(pk=request.session['borrow']).status != '1':
                raise PermissionDenied
            else:
                if request.method == "GET":
                    if id == 0:
                        context = {
                            'form': BorrowdataForm(),
                            'id_borrowdata': get_last_value('borrowdata_seq'),
                            'item': it.avaibleItem(1, 0, request.session['usergroup']),
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
                            'item': it.avaibleItem(1, 0, request.session['usergroup']),
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
                        formqty = request.POST['quantity']
                        formitem = request.POST['item']
                        item = it.avaibleItem(
                            1, 0, request.session['usergroup'])
                        for i in item:
                            if i['item'] == formitem:
                                if i['qty'] < int(formqty):
                                    messages.error(
                                        request, 'Item quantity exceeded the limit !')
                                    return redirect('borrowdataCreate')
                                else:
                                    qtyBorrow = list(BorrowData.objects.filter(
                                        borrow=request.session['borrow'], deleted=0, userGroup=request.session['usergroup']).values_list('item__id'))
                                    j = 0
                                    while j < len(qtyBorrow):
                                        if qtyBorrow[j][0] == formitem:
                                            bor = BorrowData.objects.filter(
                                                item=i['item'], borrow=request.session['borrow'], userGroup=request.session['usergroup'], deleted=0)
                                            borqty = bor.first().quantity
                                            if id == 0:
                                                bor.update(
                                                    quantity=borqty + int(formqty))
                                                return redirect('borrowView', id=request.session['borrow'])
                                            else:
                                                bor.update(
                                                    quantity=int(formqty))
                                                return redirect('borrowView', id=request.session['borrow'])
                                        j += 1
                                    form.save()
                                    if id == 0:
                                        get_next_value('borrowdata_seq')
                                    return redirect('borrowView', id=request.session['borrow'])


def borrowdataDelete(request, id):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        if request.session['role'] == "OPR":
            raise PermissionDenied
        else:
            borrowdata = BorrowData.objects.filter(
                pk=id, userGroup=request.session['usergroup'], deleted=0)
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
                pk=request.session['borrow'], deleted=0, userGroup=request.session['usergroup']).first()
            if borrow.status == '1':
                Borrow.objects.filter(
                    pk=request.session['borrow'], deleted=0,userGroup=request.session['usergroup']).update(status='2')
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
                    pk=request.session['borrow'], deleted=0,userGroup=request.session['usergroup']).update(status='4')
                ItemData.objects.filter(
                    borrow=request.session['borrow'], deleted=0,userGroup=request.session['usergroup']).update(borrow=None, status='1')
                return redirect('borrowView', id=request.session['borrow'])
            else:
                raise PermissionDenied


class PdfBorrow(View):
    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(Borrow, pk=kwargs['pk'])
        if obj.status == '1':
            raise PermissionDenied
        else:
            datas = list(BorrowData.objects.all().select_related(
                'borrow').filter(borrow=obj, deleted=0, userGroup=request.session['usergroup']).values_list('id', 'item__name', 'quantity',))
            ug = UserGroup.objects.get(pk=request.session['usergroup'])
            pdf = render_to_pdf('inside/wmsBorrow/pdf_borrow.html',
                                {'datas': datas, 'obj': obj, 'ug': ug})
            if pdf:
                response = HttpResponse(pdf, content_type='application/pdf')
                filename = "BorrowData-%s.pdf" % (12341231)
                content = "inline; filename=%s" % (filename)
                download = request.GET.get("download")
                if download:
                    content = "attachment; filename=%s" % (filename)
                response['Content-Disposition'] = content
                return response
            return HttpResponse("Not Found")
