from django.shortcuts import render, redirect
from .models import Userdata

from django.contrib.sessions.backends.db import SessionStore
from django.contrib import messages

from django.http import HttpResponseNotFound
from django.core.exceptions import PermissionDenied

from pprint import pprint


def index(request):
    if '0' not in request.session and '1' not in request.session and '2' not in request.session:
        return redirect('login')
    else:
        role = request.session['2']
        username = request.session['1']
        context = {
            'title': 'Home | WMS Poltekpos',
            'role': role,
            'username': username,
        }
        return render(request, "content/index.html", context)


def login(request):
    context = {
        'title': 'Welcome | WMS Poltekpos'
    }
    if '0' in request.session and '1' in request.session and '2' in request.session:
        return redirect('home')
    else:
        if request.method == 'POST':
            try:
                m = Userdata.objects.get(username=request.POST['username'])
            except Userdata.DoesNotExist:
                messages.error(request, 'username does not exists!')
                return redirect('login')
            n = str(m.roleid)
            level = n[13:-1]
            password = request.POST['password']
            password2 = m.password
            pass_model = password2.split(" ")[0]
            if pass_model == password:
                request.session[0] = m.id
                request.session[1] = m.username
                request.session[2] = level
                return redirect('home')
            else:
                messages.error(request, 'username or password is not correct!')
                return redirect('login')
    return render(request, "login/login_form.html", context)


def logout(request):
    try:
        del request.session['0']
        del request.session['1']
        del request.session['2']
        return redirect('login')
    except KeyError:
        pass


def usermanagement(request):
    if '0' not in request.session and '1' not in request.session and '2' not in request.session:
        return redirect('login')
    else:
        level = request.session['2']
        if level == 'OPR':
            # return HttpResponseNotFound('<h1>Page not found</h1>')
            raise PermissionDenied
        else:
            user = Userdata.objects.all()
            context = {
                'user': user,
            }
            return render(request, 'content/usermanagement.html', context)
