from django.shortcuts import render, redirect

from WMS.models import *

from django.http import HttpResponseRedirect, JsonResponse

from pprint import pprint

from sequences import get_next_value

from django.db import connection
from django.db import models

from datetime import datetime
from json import dumps


# Create your views here.


def scanner(request):
    data = {
        "item": list(Item.objects.all().select_related('subcategoryid').values_list('id', 'name', 'subcategoryid__name'))
    }
    datas = dumps(data)
    # if request.is_ajax():
    #     text = request.GET.get('data')
    #     return JsonResponse({'Da})
    return render(request, 'storage/index.html', {"datas": datas})


def put(request):
    data = request.POST.get('codedata', None)
    print(data)
    return JsonResponse({'code': data}, status=200)
