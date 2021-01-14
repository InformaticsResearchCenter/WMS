from django.shortcuts import render, redirect
from WMS.models import Admin, User, UserGroup, Role
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
import datetime
from django.db import IntegrityError
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
from django.core.mail import send_mail
from sequences import get_next_value, get_last_value
# Create your views here.

from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.views.generic import View
from django.urls import reverse
from pprint import pprint


def index(request):
    if 'group_is_login' in request.session:
        return render(request, "inside/wmsGroup/content/index.html")
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

        usergroup = UserGroup.objects.get(email=request.POST['email'])
        print(usergroup.active)
        if usergroup.active != '0':
            data = list(UserGroup.objects.filter(email=request.POST['email']).values(
                'id', 'password', 'name', 'limit'))

            if data[0]['password'] == request.POST['password']:
                request.session['groupId'] = data[0]['id']
                request.session['groupName'] = data[0]['name']
                request.session['groupLimit'] = str(data[0]['limit'])
                request.session['group_is_login'] = True
                return redirect('groupIndex')
            else:
                messages.error(request, 'Email atau password salah')
                return redirect('groupLogin')
        else:
            messages.error(request, 'Email belum verifikasi')
            return redirect('groupLogin')
    else:
        return render(request, "inside/wmsGroup/form/login.html")


def register(request):
    if request.method == "GET":
        return render(request, "inside/wmsGroup/form/register.html", {'id': get_last_value('usergroup_seq')})
    elif request.method == "POST":
        try:
            data = UserGroup.objects.create(
                id=request.POST['id'],
                name=request.POST['name'],
                address=request.POST['address'],
                phoneNumber=request.POST['phoneNumber'],
                postalCode=request.POST['postalCode'],
                email=request.POST['email'],
                password=request.POST['password'],
            )
            data.save()
            man_user = User.objects.create(
                name='MAN_'+request.POST['name'],
                username=request.POST['email'],
                password=request.POST['password'],
                userGroup=UserGroup.objects.get(pk=request.POST['id']),
                role=Role.objects.get(pk='MAN')
            )
            man_user.save()

            email = urlsafe_base64_encode(force_bytes(request.POST['email']))
            domain = get_current_site(request).domain
            link = reverse('activate', kwargs={'email': email})

            activate_url = 'http://'+domain+link

            email_subject = 'Activate WMS Polpos account'
            email_body = 'Hello '+request.POST['name']+' link activate is '+activate_url
            email = EmailMessage(
                email_subject,
                email_body,
                settings.EMAIL_HOST_USER,
                [request.POST['email']],
            )
            email.send(fail_silently=False)
            get_next_value('usergroup_seq')
            return redirect('groupLogin')
        except:
            messages.error(request, 'email sudah terdaftar')
            return redirect('groupRegister')
    else:
        return render(request, "inside/wmsGroup/form/register.html")


def logout(request):
    request.session.flush()
    return redirect('groupLogin')


class VerificationView(View):
    def get(self, request, email):
        email_group = str(urlsafe_base64_decode(email))
        usergroup = UserGroup.objects.filter(email=email_group[2 : -1])
        usergroup.update(active=1)
        messages.success(request, 'Verifikasi Berhasil')
        return redirect('groupLogin')