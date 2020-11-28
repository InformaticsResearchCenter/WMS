from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views


 path('supplierreturns', views.return_supplier, name="supplierreturns"),