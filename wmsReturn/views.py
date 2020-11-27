from django.shortcuts import render, redirect
import datetime
from WMS.models import *

# Create your views here.


def costumerReturnIndex(request):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        context = {
            'costumerReturn': CostumerReturn.objects.all(),
            'title': 'Outbound | WMS Poltekpos'
        }
        return render(request, "inside/wmsReturn/costumerReturnIndex.html", context)
