from django.shortcuts import render, redirect
from .models import Userdata

from django.contrib.sessions.backends.db import SessionStore

from pprint import pprint


def index(request):
    context = {
        'title': 'Home | WMS Poltekpos'
    }
    if '0' not in request.session and '1' not in request.session and '2' in request.session:
        return redirect('login')
    else:
        if request.session['2'] == 'ADM':
            return render(request, "index.html", context)
        elif request.session['2'] == 'MAN':
            return render(request, "index-MAN.html", context)
        elif request.session['2'] == 'OPR':
            return render(request, "index-OPR.html", context)
        else:
            return redirect('login')


def login(request):
    context = {
        'title': 'Welcome WMS Poltekpos'
    }
    if '0' in request.session and '1' in request.session and '2' in request.session:
        return redirect('home')
    else:
        if request.method == 'POST':
            m = Userdata.objects.get(username=request.POST['username'])
            n = str(m.roleid)
            level = n[13:-1]
            password = request.POST['password']
            password2 = m.password
            pass_model = password2.split(" ")[0]
            if pass_model == password:
                request.session[0] = m.userid
                request.session[1] = m.username
                request.session[2] = level
                pprint(level)
                return redirect('home')
            else:
                return redirect('login')

    return render(request, "login_form.html", context)


def logout(request):
    try:
        del request.session['0']
        del request.session['1']
        del request.session['2']
        return redirect('login')
    except KeyError:
        pass
