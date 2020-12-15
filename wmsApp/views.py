from django.shortcuts import render, redirect
from WMS.models import User,UserGroup,Role
from django.contrib.sessions.backends.db import SessionStore
from django.contrib import messages
from sequences import get_next_value
from django.http import HttpResponseNotFound,HttpResponse
from django.core.exceptions import PermissionDenied
from pprint import pprint
import datetime


# Create your views here.
def index(request):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        context = {
            'title': 'Home | WMS Poltekpos',
            'role': request.session['role'],
            'username': request.session['username'],
            'userGroup' : request.session['usergroup']
        }
        return render(request, "content/index.html", context)

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
        