from django.shortcuts import render

# Create your views here.

def return_supplier(request):
    if 'is_login' not in request.session or request.session['limit'] <= datetime.datetime.today().strftime('%Y-%m-%d'):
        return redirect('login')
    else:
        # context = {
        #     'role': request.session['role'],
        #     'username': request.session['username'],
        #     'title': 'Category | Inbound',
        #     'category': Category.objects.filter(deleted=0, userGroup=request.session['usergroup']).values('id', 'category')
        # }
        return render(request, 'content/return_supplier.html')
