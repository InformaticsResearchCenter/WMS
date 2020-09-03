from django.shortcuts import render, redirect

from .forms import CategoryForm
from WMS.models import Category

from pprint import pprint

from sequences import get_next_value

# Create your views here.


def category(request, id=0):
    if request.method == "GET":
        if id == 0:
            form = CategoryForm()
            cat_id = get_next_value("category_seq")
            return render(request, 'content/category.html', {'form': form, 'cat_id': cat_id})
        else:
            category = Category.objects.get(pk=id)
            form = CategoryForm(instance=category)
            return render(request, 'content/category.html', {'form': form})
    else:
        if id == 0:
            form = CategoryForm(request.POST)
        else:
            category = Category.objects.get(pk=id)
            form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('list_category')
    return render(request, 'content/category.html')


def list_category(request):
    return render(request, 'content/list_category.html', {'category': Category.objects.order_by('id')})


def category_delete(request, id):
    category = Category.objects.get(pk=id)
    category.delete()
    return redirect('list_category')


def item(request):
    return render(request, 'content/item.html')
