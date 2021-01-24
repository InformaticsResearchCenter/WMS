from django.shortcuts import render, redirect
from WMS.models import User,UserGroup,Role
from django.contrib.sessions.backends.db import SessionStore
from django.contrib import messages
from sequences import get_next_value
from django.http import HttpResponseNotFound,HttpResponse
from WMS.models import *
from django.core.exceptions import PermissionDenied
from pprint import pprint
import datetime


# Create your views here.
def index(request):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
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
        context = {
            'title': 'Home | WMS Poltekpos',
            'role': request.session['role'],
            'username': request.session['username'],
            'userGroup' : request.session['usergroup'],
            'avaibleItem' : ItemData.objects.filter(status="1", userGroup=request.session['usergroup'], deleted = 0).count(),
            'itemSold' : ItemData.objects.filter(status="2", userGroup=request.session['usergroup'], deleted = 0).count(),
            'borrowedItem' : ItemData.objects.filter(status="3", userGroup=request.session['usergroup'], deleted = 0).count(),
            'brokenItem' : ItemData.objects.filter(status="4", userGroup=request.session['usergroup'], deleted = 0).count(),
            'lostItem' : ItemData.objects.filter(status="5", userGroup=request.session['usergroup'], deleted = 0).count(),
            "detailAvaibleItem" : rawitem
        }
        return render(request, "inside/wmsApp/index.html", context)

def login(request):
    context = {
        'title': 'Welcome | WMS Poltekpos',
        'login' : 'Member',
    }
    if 'is_login' in request.session:
        return redirect('home')
    else:
        if request.method == 'POST':
            try:
                User.objects.get(username=request.POST['username'])
            except User.DoesNotExist:
                messages.error(request, 'username does not exists!')
                return redirect('login')
            
            data = list(User.objects.filter(username=request.POST['username']).values('id','username','role_id','userGroup_id','password','deleted'))
            date = list(UserGroup.objects.filter(id=data[0]['userGroup_id']).values('limit'))

            if data[0]['deleted'] == "1":
                messages.error(request, 'username does not exists!')
                return redirect('login')

            elif data[0]['password'] == request.POST['password']:
                if  datetime.datetime.today().strftime('%Y-%m-%d') <= str(date[0]['limit']) :
                    request.session['id'] = data[0]['id']
                    request.session['username'] = data[0]['username']
                    request.session['role'] = data[0]['role_id']
                    request.session['usergroup'] = data[0]['userGroup_id']
                    request.session['limit'] = str(date[0]['limit'])
                    request.session['is_login'] = True
                    return redirect('home')
                else:
                    messages.error(request, 'Expired')
                    return redirect('login')
            else:
                messages.error(request, 'username or password is not correct!')
                return redirect('login')
    return render(request, "login/login_form.html", context)


def logout(request):
    request.session.flush()
    return redirect('login')
        