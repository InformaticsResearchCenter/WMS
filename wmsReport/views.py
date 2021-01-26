from django.shortcuts import render,redirect
from WMS.models import *
from django.http import HttpResponse


# Create your views here.
def reportIndex(request):
    context = {
            'title': 'Report | WMS Poltekpos',
            'role': request.session['role'],
            'username': request.session['username'],
            'userGroup' : request.session['usergroup'],
            'avaibleItem' : ItemData.objects.filter(status="1", userGroup=request.session['usergroup'], deleted = 0).count(),
            'itemSold' : ItemData.objects.filter(status="2", userGroup=request.session['usergroup'], deleted = 0).count(),
            'borrowedItem' : ItemData.objects.filter(status="3", userGroup=request.session['usergroup'], deleted = 0).count(),
            'brokenItem' : ItemData.objects.filter(status="4", userGroup=request.session['usergroup'], deleted = 0).count(),
            'lostItem' : ItemData.objects.filter(status="5", userGroup=request.session['usergroup'], deleted = 0).count(),
    }
    return render(request,'inside/wmsReport/index.html', context)