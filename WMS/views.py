from django.shortcuts import render, redirect
from .models import Userdata

from django.contrib.sessions.backends.db import SessionStore


def index(request):
    if '0' not in request.session and '1' not in request.session and '2' not in request.session:
        return redirect('login')
    else:
        role = request.session['2']
        context = {
            'title': 'Home | WMS Poltekpos',
            'role': role,
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
            m = Userdata.objects.get(username=request.POST['username'])
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
