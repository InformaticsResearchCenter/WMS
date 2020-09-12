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
    # ------------------ Category and Subcategory ----------------
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


    # --------------------- SUPPLIER ------------------
    path('supplier/', views.list_supplier, name="list_supplier"),
    path('supplier/add_supplier/', views.supplier, name="add_supplier"),
    path('update_supplier/<slug:id>/', views.supplier, name="update_supplier"),
    path('supplier/delete/<slug:id>/',
         views.supplier_delete, name="delete_supplier"),
    path('supplier/detail/<slug:id>/',
         views.supplier_detail, name="detail_supplier"),

    # ----------------------- Item ---------------------
    path('item/', views.main_item, name="item"),
    path('item/add_item/', views.item, name="add_item"),
    path('item/delete_item/<slug:id>/', views.delete_item, name="delete_item"),
    path('item/update_item/<slug:id>/', views.item, name='update_item'),


    # -------------------- Inbound --------------------------
    path('inbound/', views.main_inbound, name="inbound"),
    path('inbound/add_inbound', views.inbound, name="add_inbound"),
    path('inbound/delete_inbound/<slug:id>/',
         views.delete_inbound, name="delete_inbound"),
    path('inbound/view_inbound/<slug:id>/',
         views.view_inbound, name="view_inbound"),
    path('inbound/confirm/',
         views.confirm, name="confirm"),

    # -------------------- Itemdata --------------------------
    path('inbound/add_itemdata', views.item_data, name="add_itemdata"),
    path('inbound/update_itemdata/<slug:id>/',
         views.item_data, name="update_itemdata"),
    path('inbound/delete_itemdata/<slug:id>/',
         views.delete_itemdata, name="delete_itemdata"),
]
