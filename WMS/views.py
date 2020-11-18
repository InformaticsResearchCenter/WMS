from django.shortcuts import render, redirect
from .forms import *
from .models import User,UserGroup,Role
from django.contrib.sessions.backends.db import SessionStore
from django.contrib import messages
from sequences import get_next_value
from django.http import HttpResponseNotFound,HttpResponse
from django.core.exceptions import PermissionDenied
from pprint import pprint
import datetime


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
        'title': 'Welcome | WMS Poltekpos'
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
    try:
        del request.session['id']
        del request.session['username']
        del request.session['role']
        del request.session['usergroup']
        del request.session['is_login']
        return redirect('login')
    except KeyError:
        pass


# def usermanagement(request):
#     if '0' not in request.session and '1' not in request.session and '2' not in request.session:
#         return redirect('login')
#     else:
#         level = request.session['2']
#         if level != "MAN":
#             raise PermissionDenied
#         else:
#             user = Userdata.objects.all()
#             context = {
#                 'user': user,
#                 'title': 'User Management | WMS POLTEKPOS',
#             }
#             return render(request, 'content/usermanagement.html', context)


# def delete_user(request, id):
#     if '0' not in request.session and '1' not in request.session and '2' not in request.session:
#         return redirect('login')
#     else:
#         user = Userdata.objects.get(pk=id)
#         user.delete()
#         return redirect('user')


# #------------------------- User --------       

# def userdata(request, id=0):
#     if '0' not in request.session and '1' not in request.session and '2' not in request.session:
#         return redirect('login')
#     else:
#         if request.method == "GET":
#             if id == 0:
#                 form = UserdataForm()
#                 roleid = Role.objects.all()
#                 user_id = get_next_value("user_seq")
#                 username = request.session['1']
#                 context = {
#                     'form': form,
#                     'roleid': roleid,
#                     'user_id': user_id,
#                     'username': username,
#                     'title': 'Add User'
#                 }
#                 return render(request, 'content/userdata.html', context)
#             else:
#                 user = Userdata.objects.get(pk=id)
#                 roleid = Role.objects.all()
#                 form = UserdataForm(instance=user)
#                 context = {
#                     'form': form,
#                     'user': user,
#                     'roleid': roleid,
#                     'title': 'Update Userdata'
#                 }
#             return render(request, 'content/update_user.html', context)
#         else:
#             if id == 0:
#                 form = UserdataForm(request.POST)
#             else:
#                 userdata = Userdata.objects.get(pk=id)
#                 form = UserdataForm(request.POST, instance=userdata)
#             if form.is_valid():
#                 form.save()
#                 return redirect('user')
#         return render(request, 'content/userdata.html')
#         level = request.session['2']
#         if level != "MAN":
#             raise PermissionDenied
#         else:
#             user = Userdata.objects.get(pk=id)
#             user.delete()
#             return redirect('user')
