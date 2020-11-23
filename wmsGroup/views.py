from django.shortcuts import render, redirect
from WMS.models import Admin,User,UserGroup,Role
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
import datetime
from django.db import IntegrityError
from django.contrib import messages

# Create your views here.
def index(request):
    if 'group_is_login' in request.session:
        return render(request,"inside/wmsGroup/content/index.html")
    else:
        return redirect('groupLogin')


def login(request):
    if request.method == "GET":
        return render(request, "inside/wmsGroup/form/login.html")
    elif request.method == "POST":
        try:
            UserGroup.objects.get(email=request.POST['email'])
        except:
            messages.error(request, 'Email tidak terdaftar')
            return redirect('groupLogin')

        data = list(UserGroup.objects.filter(email=request.POST['email']).values('id','password','name','limit'))

        if data[0]['password'] == request.POST['password']:
            request.session['groupId'] = data[0]['id']
            request.session['groupName'] = data[0]['name']
            request.session['groupLimit'] = str(data[0]['limit'])
            request.session['group_is_login'] = True
        return redirect('groupIndex')
    else:
        return render(request, "inside/wmsGroup/form/login.html")

def register(request):
    if request.method == "GET":
        return render(request, "inside/wmsGroup/form/register.html")
    elif request.method == "POST":
        try:
            data = UserGroup.objects.create(
                name=request.POST['name'],
                address=request.POST['address'],
                phoneNumber=request.POST['phoneNumber'],
                postalCode=request.POST['postalCode'],
                email=request.POST['email'],
                password=request.POST['password'],
            )
            data.save()
            return redirect('groupLogin')
        except:
            messages.error(request, 'email sudah terdaftar')
            return redirect('groupRegister')
    else:
        return render(request, "inside/wmsGroup/form/register.html")
    

def logout(request):
    request.session.flush()
    return redirect('groupLogin')