from django.shortcuts import render,redirect
from WMS.models import *
from django.http import HttpResponse
from django.core.paginator import Paginator


# Create your views here.
def reportIndex(request):
    context = {
            'title': 'Report | WMS Poltekpos',
            'role': request.session['role'],
            'username': request.session['username'],
            'userGroup' : request.session['usergroup'],
            'stagingArea' : ItemData.objects.filter(status="0", userGroup=request.session['usergroup'], deleted = 0).count(),
            'avaibleItem' : ItemData.objects.filter(status="1", userGroup=request.session['usergroup'], deleted = 0).count(),
            'itemSold' : ItemData.objects.filter(status="2", userGroup=request.session['usergroup'], deleted = 0).count(),
            'borrowedItem' : ItemData.objects.filter(status="3", userGroup=request.session['usergroup'], deleted = 0).count(),
            'brokenItem' : ItemData.objects.filter(status="4", userGroup=request.session['usergroup'], deleted = 0).count(),
            'lostItem' : ItemData.objects.filter(status="5", userGroup=request.session['usergroup'], deleted = 0).count(),
			'log' : Log.objects.filter(userGroup=request.session['usergroup'], deleted = 0).values()
    }
    return render(request,'inside/wmsReport/index.html', context)

def log(request):
    context = {
            'title': 'Report | WMS Poltekpos',
            'role': request.session['role'],
            'username': request.session['username'],
            'userGroup' : request.session['usergroup'],
			'log' : Log.objects.filter(userGroup=request.session['usergroup'], deleted = 0).values('id', 'detail', 'item__name', 'item__size', 'item__colour', 'quantity', 'user__username', 'date')
    }
    return render(request,'inside/wmsReport/log.html', context)

def reportDetail(request,status):

	item=Item.objects.filter(userGroup=request.session['usergroup']).values()
	data=ItemData.objects.filter(status=status, userGroup=request.session['usergroup'], deleted = 0).values('id','inbound__item__name','binlocation__binlocation', 'inbound__inbound__date').order_by('-inbound__inbound__date')

	# p = Paginator(data, 20)

	# page = p.page(1)
	context = {
		'title': 'Report | WMS Poltekpos',
		'role': request.session['role'],
		'username': request.session['username'],
		'userGroup' : request.session['usergroup'],
		'item' : data,
		'quantity' : ItemData.objects.filter(status=status, userGroup=request.session['usergroup'], deleted = 0).count()
	}
	
	return render(request,'inside/wmsReport/report.html', context)
