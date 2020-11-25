from django.shortcuts import render, redirect
from WMS.models import Admin,User,UserGroup,Role
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
import datetime
from django.db import IntegrityError
from django.contrib import messages

# Create your views here.

def index(request):
    if 'admin_is_login' not in request.session:
        return redirect('adminLogin')
    else:
        data = list(UserGroup.objects.values())
        limit = datetime.datetime.today().strftime('%Y-%m-%d')
        for i in range(len(data)):
            data[i]['limit'] = str(data[i]['limit'])

        context = {
            "data" : data,
            "limit" : limit,
        }
        return render(request,'inside/wmsAdmin/index.html', context=context)
    return redirect('adminLogin')

def login(request):
    context = {
        'title': 'Welcome | WMS Poltekpos',
        'login' : 'Admin',
    }
    if 'admin_is_login' in request.session:
        return redirect('adminIndex')
    else:
        if request.method == 'POST':
            try:
                Admin.objects.get(username=request.POST['username'])
            except Admin.DoesNotExist:
                messages.error(request, 'username does not exists!')
                return redirect('adminLogin')
            data = list(Admin.objects.filter(username=request.POST['username']).values('id','username','password','deleted'))
            print(data)
            print(request.POST['password'])

            if data[0]['deleted'] == "1":
                messages.error(request, 'username does not exists!')
                return redirect('login')

            elif data[0]['password'] == request.POST['password']:
                request.session['adminId'] = data[0]['id']
                request.session['adminUsername'] = data[0]['username']
                request.session['admin_is_login'] = True
                return redirect('adminIndex')
            else:
                messages.error(request, 'username or password is not correct!')
                return redirect('adminLogin')
    return render(request, "login/login_form.html", context)


def logout(request):
    request.session.flush()
    return redirect('adminLogin')

    # try:
    #     del request.session['adminId']
    #     del request.session['adminUsername']
    #     del request.session['admin_is_login']
    #     return redirect('adminLogin')
    # except KeyError as e:
    #     return HttpResponse(e)

def limit(request,id):
    if 'admin_is_login' not in request.session:
        return redirect('adminLogin')
    else:
        print(id)
        print(request.POST['limit'])
        UserGroup.objects.filter(pk=id).update(
                limit=request.POST['limit']
                )
    return redirect("adminIndex")
        
def deactive(request,id):
    if 'admin_is_login' not in request.session:
        return redirect('adminLogin')
    else:
        print(id)
        UserGroup.objects.filter(pk=id).update(
                limit="1000-10-10"
                )
    return redirect("adminIndex")
        