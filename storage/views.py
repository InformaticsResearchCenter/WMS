from django.shortcuts import render

# Create your views here.
def scanner(request):
    return render(request, 'storage/index.html')