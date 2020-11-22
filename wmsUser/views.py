from django.shortcuts import render, redirect
from WMS.models import User, UserGroup, Role
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
import datetime
from django.db import IntegrityError
from django.contrib import messages
# from sequences import Sequence
from sequences import get_next_value
from WMS.forms import UserForm

def index(request):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        if request.session['role'] != "MAN":
            raise PermissionDenied
        else:
            user = User.objects.filter(userGroup=request.session['usergroup'], deleted='0').values(
                'id', 'username', 'name', 'address', 'postalCode', 'deleted', 'phoneNumber', 'role_id')
            context = {
                'title': 'Home | WMS Poltekpos',
                'role': request.session['role'],
                'username': request.session['username'],
                'userGroup': request.session['usergroup'],
                'user': user
            }
            return render(request, 'inside/wmsUser/index.html', context=context)


def user(request, id=0):
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
                if request.method == "GET":
                    if id == 0:
                        context = {
                            'form': UserForm(),
                            'group_id': request.session['usergroup'],
                            'role_data': Role.objects.all(),
                            'role': request.session['role'],
                            'username': request.session['username'],
                            'title': 'Add User | User Management'
                        }
                        return render(request, 'inside/wmsUser/userCreate.html', context)
                    else:
                        user = User.objects.get(pk=id)
                        context = {
                            'form': UserForm(instance=user),
                            'user': user,
                            'role_data': Role.objects.all(),
                            'role': request.session['role'],
                            'group_id': request.session['usergroup'],
                            'username': request.session['username'],
                            'title': 'Update User | User Management'
                        }
                        return render(request, 'inside/wmsUser/userUpdate.html', context)
                else:
                    if id == 0:
                        form = UserForm(request.POST)
                    else:
                        user = User.objects.get(pk=id)
                        form = UserForm(request.POST, instance=user)
                    if form.is_valid():
                        if request.POST['role'] != "MAN":
                            form.save()
                            return redirect('userIndex')
                        else:
                            messages.error(
                                request, "Can't add user role MAN !")
                            return redirect('userIndex')
                return render(request, 'inside/wmsUser/userCreate.html')
            except IntegrityError as e:
                messages.error(request, 'Exist')
                return redirect('userIndex')


def user_delete(request, id):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        if request.session['role'] != "MAN":
            raise PermissionDenied
        else:
            User.objects.filter(pk=id).update(deleted=1)
            return redirect('userIndex')
