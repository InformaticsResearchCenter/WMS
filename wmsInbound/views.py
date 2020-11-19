from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied
import datetime
from WMS.models import *
from WMS.forms import CategoryForm, SubcategoryForm

# Create your views here.


def itemIndex(request):
    return render(request, 'inside/wmsInbound/itemIndex.html')

# ==================== CATEGORY ======================


def categoryIndex(request):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        context = {
            'role': request.session['role'],
            'username': request.session['username'],
            'title': 'Category | Inbound',
            'category': Category.objects.filter(deleted=0, userGroup=request.session['usergroup']).values('id', 'category')
        }
        return render(request, 'inside/wmsInbound/categoryIndex.html', context)


def category(request, id=0):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        if request.session['role'] == "OPR":
            raise PermissionDenied
        else:
            if request.method == "GET":
                if id == 0:
                    context = {
                        'form': CategoryForm(),
                        'group_id': request.session['usergroup'],
                        'role': request.session['role'],
                        'username': request.session['username'],
                        'title': 'Add Category | Inbound'
                    }
                    return render(request, 'inside/wmsInbound/categoryCreate.html', context)
                else:
                    category = Category.objects.get(pk=id)
                    context = {
                        'form': CategoryForm(instance=category),
                        'category': category,
                        'role': request.session['role'],
                        'group_id': request.session['usergroup'],
                        'username': request.session['username'],
                        'title': 'Update Category | Inbound'
                    }
                    return render(request, 'inside/wmsInbound/categoryUpdate.html', context)
            else:
                if id == 0:
                    form = CategoryForm(request.POST)
                else:
                    category = Category.objects.get(pk=id)
                    form = CategoryForm(request.POST, instance=category)
                if form.is_valid():
                    form.save()
                    return redirect('categoryIndex')


def category_delete(request, id):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        if request.session['role'] == "OPR":
            raise PermissionDenied
        else:
            Category.objects.filter(pk=id).update(deleted=1)
            return redirect('categoryIndex')


# ============================= SUBCATEGORY =================================

def subcategoryIndex(request, id):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        request.session['category'] = id
        context = {
            'id': Category.objects.get(pk=id),
            'role': request.session['role'],
            'username': request.session['username'],
            'title': 'Subcategory | Inbound',
            'subcategory': Subcategory.objects.filter(deleted=0, userGroup=request.session['usergroup'], category=id).values('id', 'subcategory', 'category_id')
        }
        return render(request, 'inside/wmsInbound/subcategoryIndex.html', context)


def subcategory(request, id=0):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        if request.session['role'] == "OPR":
            raise PermissionDenied
        else:
            if request.method == "GET":
                if id == 0:
                    context = {
                        'form': SubcategoryForm(),
                        'category': Category.objects.get(pk=request.session['category']),
                        'group_id': request.session['usergroup'],
                        'role': request.session['role'],
                        'username': request.session['username'],
                        'title': 'Add Subcategory | Inbound'
                    }
                    return render(request, 'inside/wmsInbound/subcategoryCreate.html', context)
                else:
                    subcategory = Subcategory.objects.get(pk=id)
                    context = {
                        'form': SubcategoryForm(instance=subcategory),
                        'subcategory': subcategory,
                        'role': request.session['role'],
                        'group_id': request.session['usergroup'],
                        'username': request.session['username'],
                        'title': 'Update Subcategory | Inbound'
                    }
                    return render(request, 'inside/wmsInbound/subcategoryUpdate.html', context)
            else:
                if id == 0:
                    form = SubcategoryForm(request.POST)
                else:
                    subcategory = Subcategory.objects.get(pk=id)
                    form = SubcategoryForm(request.POST, instance=subcategory)
                if form.is_valid():
                    form.save()
                    return redirect('subcategoryIndex', id=request.session['category'])


def subcategoryDelete(request, id):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        if request.session['role'] == "OPR":
            raise PermissionDenied
        else:
            Subcategory.objects.filter(pk=id).update(deleted=1)
            return redirect('subcategoryIndex', id=request.session['category'])
