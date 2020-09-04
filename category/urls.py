"""WMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.list_category, name="list_category"),
    path('add_category/', views.main_category, name="add_category"),
    path('add_subcategory/', views.main_subcategory, name="add_subcategory"),
    path('update_category/<slug:id>/',
         views.main_category, name="update_category"),
    path('update_subcategory/<slug:id>/',
         views.main_subcategory, name="update_subcategory"),
    path('view_category/<slug:id>/',
         views.view_category, name="view_category"),
    path('delete_category/<slug:id>/',
         views.delete_category, name="delete_category"),
    path('delete_subcategory/<slug:id>/',
         views.delete_subcategory, name="delete_subcategory"),
    path('item/', views.main_item, name="item"),
]
