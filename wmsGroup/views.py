from django.shortcuts import render, redirect
from WMS.models import *
from WMS.forms import *
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
from .utils import token_generator
from pprint import pprint


def main_usergroup(request):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        context = {
            'usergroup': UserGroup.objects.all(),
            'title': 'UserGroup | WMS Poltekpos'
        }
        return render(request, "inside/wmsGroup/data_usergroup.html", context)        

def edit_usergroup(request):    
    return render(request, "inside/wmsGroup/form/edit_usergroup.html")

def index(request):
    if 'group_is_login' in request.session:
        return render(request, "inside/wmsGroup/content/index.html")
    else:
        return redirect('groupLogin')


def login(request):
    if request.method == "GET":
        context = {
            'title': 'Login Group'
        }
        return render(request, "inside/wmsGroup/form/login.html", context)
    elif request.method == "POST":
        try:
            UserGroup.objects.get(email=request.POST['email'])
        except:
            messages.error(request, 'Email tidak terdaftar')
            return redirect('groupLogin')

        usergroup = UserGroup.objects.get(email=request.POST['email'])
        # angka 2 ganti dengan 0
        if usergroup.active != '2':
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
        context = {
            'title': 'Login Group'
        }
        return render(request, "inside/wmsGroup/form/login.html", context)


def registerr(request, id=0):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        if request.session['role'] == "OPR":
            raise PermissionDenied
        else:
            if request.method == "GET":
                if id == 0:
                    context = {
                        'form': UserGroupForm(),
                        'title': 'Register Akun',
                        'id': get_last_value('usergroup_seq')
                    }
                    return render(request, 'inside/wmsGroup/form/register.html', context)
                else:
                    print(gagal)
                    # supplier = Supplier.objects.get(pk=id)
                    # context = {
                    #     'form': SupplierForm(instance=supplier),
                    #     'supplier': supplier,
                    #     'group_id': request.session['usergroup'],
                    #     'username': request.session['username'],
                    #     'role': request.session['role'],
                    #     'title': 'Update Supplier | Inbound'
                    # }
                return render(request, 'inside/wmsGroup/form/register.html', context)
            else:
                if id == 0:
                    form = UserGroupForm(request.POST)
                else:
                    usergroup = UserGroup.objects.get(pk=id)
                    form = UserGroupForm(request.POST, instance=usergroup)
                if form.is_valid():
                    form.save()
                    man_user = User.objects.create(
                        name='MAN_'+request.POST['name'],
                        username=request.POST['email'],
                        password=request.POST['password'],
                        userGroup=UserGroup.objects.get(pk=request.POST['id']),
                        role=Role.objects.get(pk='MAN')
                    )
                    man_user.save()
                    if id == 0:
                        get_next_value('usergroup_seq')
                    return redirect('groupLogin')
            return render(request, 'inside/wmsGroup/form/register.html')


def register(request):
    if request.method == "GET":
        context = {
            'title': 'Register Akun',
            'id': get_last_value('usergroup_seq')
        }
        return render(request, "inside/wmsGroup/form/register.html", context)
    elif request.method == "POST":
        # try:
        data = UserGroup.objects.create(
            id=request.POST['id'],
            name=request.POST['name'],
            address=request.POST['address'],
            phoneNumber=request.POST['phoneNumber'],
            postalCode=request.POST['postalCode'],
            email=request.POST['email'],
            password=request.POST['password'],
            city=request.POST['city'],
            districts=request.POST['districts'],
            province=request.POST['province'],
            addressCompany=request.POST['addressCompany'],
            imageCompany=request.POST['imageCompany'],
            nameCompany=request.POST['nameCompany'],
            profileOperator=request.POST['profileOperator'],
            village=request.POST['village'],
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

        # email = urlsafe_base64_encode(force_bytes(request.POST['email']))
        # domain = get_current_site(request).domain
        # token = token_generator.make_token(request.POST['phoneNumber'])
        # link = reverse('activate', kwargs={'email': email, 'token': token})
        # usergroup = UserGroup.objects.filter(email=request.POST['email'])
        # usergroup.update(token=token)
        # activate_url = 'http://'+domain+link

        # email_subject = 'Activate WMS Polpos account'
        # email_body = 'Hello '+request.POST['name']+' link activate is '+activate_url
        # email = EmailMessage(
        #     email_subject,
        #     email_body,
        #     settings.EMAIL_HOST_USER,
        #     [request.POST['email']],
        # )
        # email.send(fail_silently=False)
        get_next_value('usergroup_seq')
        return redirect('groupLogin')
        # except:
        #     messages.error(request, 'email sudah terdaftar')
        #     return redirect('groupRegister')
    else:
        context = {
            'title': 'Register Akun'
        }
        return render(request, "inside/wmsGroup/form/register.html", context)


def resetPassword(request):
    if request.method == "POST":
        try:
            usergroup = UserGroup.objects.get(email=request.POST['email'])
        except:
            messages.error(request, 'Email belum terdaftar')
            return redirect('groupRegister')
        email = urlsafe_base64_encode(force_bytes(request.POST['email']))
        domain = get_current_site(request).domain
        token = token_generator.make_token(usergroup.phoneNumber)
        link = reverse('reset', kwargs={'email': email, 'token': token})
        usergrouptoken = UserGroup.objects.filter(email=request.POST['email'])
        usergrouptoken.update(token=token)
        activate_url = 'http://'+domain+link

        email_subject = 'Resset Passwrod WMS Poltekpos account'
        email_body = 'Hello '+usergroup.name+' link Reset is '+activate_url
        email = EmailMessage(
            email_subject,
            email_body,
            settings.EMAIL_HOST_USER,
            [request.POST['email']],
        )
        email.send(fail_silently=False)
        return redirect('groupLogin')
    else:
        context = {
            'title': 'Reset Password'
        }
        return render(request, "inside/wmsGroup/form/resetpassword.html", context)
    context = {
        'title': 'Reset Password'
    }
    return render(request, "inside/wmsGroup/form/resetpassword.html", context)


def logout(request):
    request.session.flush()
    return redirect('groupLogin')


class VerificationView(View):
    def get(self, request, email, token):
        email_group = str(urlsafe_base64_decode(email))
        usergroup = UserGroup.objects.filter(email=email_group[2 : -1])
        getusergroup = usergroup.first()
        if getusergroup.token == token:
            usergroup.update(active=1)
            messages.success(request, 'Verifikasi Berhasil')
            return redirect('groupLogin')
        else:
            messages.success(request, 'Token url anda Salah')
            return redirect('groupLogin') 


class ResetPassword(View):
    def get(self, request, email, token):
        context = {
            'title': 'New Password'
        }
        return render(request, "inside/wmsGroup/form/password.html", context)
    

    def post(self, request, email, token):
        email_group = str(urlsafe_base64_decode(email))
        usergroup = UserGroup.objects.filter(email=email_group[2 : -1])
        getusergroup = usergroup.first()
        if getusergroup.token == token:
            usergroup.update(password=request.POST['password'])
            messages.success(request, 'Reset Berhasil')
            return redirect('groupLogin')            
        else:
            messages.success(request, 'Token url anda Salah')
            return redirect('groupReset') 