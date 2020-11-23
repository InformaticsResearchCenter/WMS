from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied
import datetime
from WMS.models import *
from WMS.forms import RackForm
from django.db.models import Count
from django.db.models import Max


# ===================================== RACK =========================================
def rackIndex(request):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        context = {
            'role': request.session['role'],
            'group_id': request.session['usergroup'],
            'username': request.session['username'],
            'title': 'Rack | Inbound',
            'rack': Rack.objects.filter(deleted=0, userGroup=request.session['usergroup']).annotate(numbin=Count('binlocation')).order_by('id')
        }
        return render(request, 'inside/wmsStorage/rackIndex.html', context)


def rack(request):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        role = request.session['role']
        if role == 'OPR':
            raise PermissionDenied
        else:
            if request.method == "GET":
                context = {
                    'form': RackForm(),
                    'role': role,
                    'group_id': request.session['usergroup'],
                    'username': request.session['username'],
                    'title': 'Add Rack',
                }
                return render(request, 'inside/wmsStorage/rackCreate.html', context)
            else:
                form = RackForm(request.POST)
                if form.is_valid():
                    form.save()
                    numberbin = int(
                        request.POST['row']) * int(request.POST['col'])
                    data_bin = []
                    for i in range(int(numberbin)):
                        bin_id = request.POST['id']+(str(i+1))
                        data_bin.append(Binlocation(id=bin_id, rack=Rack.objects.get(pk=request.POST['id']),
                                                    capacity=request.POST['capacity']))
                    Binlocation.objects.bulk_create(data_bin)
                    print(data_bin)
                    return redirect('rackIndex')
                # query = """INSERT INTO Binlocation(id, rackid, capacity)
                # VALUES
                # (%s, %s, %s) """
                # cursor.executemany(query, data_bin)
                # return redirect('rack')

            return render(request, 'storage/rack.html')
