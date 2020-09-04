from django.shortcuts import render, redirect

from .forms import CategoryForm, SubcategoryForm
from WMS.models import Category, Subcategory

from django.http import HttpResponseRedirect

from pprint import pprint

from sequences import get_next_value

# Create your views here.


def main_category(request, id=0):
    if '0' not in request.session and '1' not in request.session and '2' not in request.session:
        return redirect('login')
    else:
        if request.method == "GET":
            if id == 0:
                form = CategoryForm()
                cat_id = get_next_value("category_seq")
                return render(request, 'content/category.html', {'form': form, 'cat_id': cat_id})
            else:
                category = Category.objects.get(pk=id)
                form = CategoryForm(instance=category)
                return render(request, 'content/update_category.html', {'form': form, 'category': category})
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
    if '0' not in request.session and '1' not in request.session and '2' not in request.session:
        return redirect('login')
    else:
        return render(request, 'content/list_category.html', {'category': Category.objects.order_by('id')})


def delete_category(request, id):
    if '0' not in request.session and '1' not in request.session and '2' not in request.session:
        return redirect('login')
    else:
        category = Category.objects.get(pk=id)
        category.delete()
        return redirect('list_category')


def delete_subcategory(request, id):
    if '0' not in request.session and '1' not in request.session and '2' not in request.session:
        return redirect('login')
    else:
        subcategory = Subcategory.objects.get(pk=id)
        subcategory.delete()
        return redirect('list_category')


def main_item(request):
    if '0' not in request.session and '1' not in request.session and '2' not in request.session:
        return redirect('login')
    else:
        return render(request, 'content/main_item.html')


def view_category(request, id):
    if '0' not in request.session and '1' not in request.session and '2' not in request.session:
        return redirect('login')
    else:
        subcategory = Subcategory.objects.all().filter(categoryid=id)
        request.session['cat_id'] = id
        cat_id = request.session['cat_id']
        context = {
            'title': 'View Category - Subcategory',
            'subcategory': subcategory,
            'cat_id': cat_id
        }
        return render(request, 'content/view_category.html', context)


def main_subcategory(request, id=0):
    if '0' not in request.session and '1' not in request.session and '2' not in request.session:
        return redirect('login')
    else:
        if request.method == "GET":
            if id == 0:
                form = SubcategoryForm()
                subcat_id = get_next_value("subcategory_seq")
                cat_id = request.session['cat_id']
                context = {
                    'form': form,
                    'subcat_id': subcat_id,
                    'cat_id': cat_id
                }
                return render(request, 'content/subcategory.html', context)
            else:
                subcategory = Subcategory.objects.get(pk=id)
                str_subcat_id = str(subcategory.categoryid)
                subcat_id = str_subcat_id[17:-1]
                form = SubcategoryForm(instance=subcategory)
                context = {
                    'subcategory': subcategory,
                    'subcat_id': subcat_id,
                    'form': form
                }
                return render(request, 'content/update_subcategory.html', context)
        else:
            if id == 0:
                form = SubcategoryForm(request.POST)
            else:
                subcategory = Subcategory.objects.get(pk=id)
                form = SubcategoryForm(request.POST, instance=subcategory)
            if form.is_valid():
                cat_id = request.session['cat_id']
                form.save()
                return redirect('view_category', id=cat_id)
        return render(request, 'content/subcategory.html')
