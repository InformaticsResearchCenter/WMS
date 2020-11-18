from django.shortcuts import render, redirect
from WMS.models import User,UserGroup, Role
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
import datetime
from django.db import IntegrityError
from django.contrib import messages
# from sequences import Sequence
from sequences import get_next_value


def index(request):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        if request.session['role'] != "MAN":
            raise PermissionDenied
        else:
            user = User.objects.filter(userGroup=request.session['usergroup']).values('username','name','address','postalCode','phoneNumber', 'role_id')
            print(user)
        context = {
            'title': 'Home | WMS Poltekpos',
            'role': request.session['role'],
            'username': request.session['username'],
            'userGroup' : request.session['usergroup'],
            'user' : user
        }
        return render(request, 'inside/wmsUser/index.html', context=context)

def create(request):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        if request.session['role'] != "MAN":
            raise PermissionDenied
        else:
            try:
                data = User(
                    name="Administrator",address='jl. kemana',phoneNumber='08679584738', postalCode='712739', username="administrator1", password="administrator1", role=Role.objects.get(pk="ADM"), userGroup=UserGroup.objects.get(pk=request.session['usergroup'])
                    )
                data.save()
                last = get_next_value('user_seq')
                print(last)
                next('user_seq')
                print(last)
            except IntegrityError as e:
                messages.error(request, 'Exist')
                return redirect('userIndex')

def update(request):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        if request.session['role'] != "MAN":
            raise PermissionDenied
        else:
            data = User.objects.filter(pk=4).update(
                    name="Administrator",address='jl. kemana',phoneNumber='08679584738', postalCode='712739', username="administrator3", password="administrator3", role=Role.objects.get(pk="ADM"), userGroup=UserGroup.objects.get(pk=request.session['usergroup'])
                    )
            return redirect('userIndex')

        

def delete(request):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        if request.session['role'] != "MAN":
            raise PermissionDenied
        else:
            data = User.objects.filter(pk=4).update(
                    deleted=1
                    )
            return redirect('userIndex')



