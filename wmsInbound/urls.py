from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    # ============================ ITEM ===============================
    path('item/', views.itemIndex, name="itemIndex"),
    path('item/item_create', views.item, name="itemCreate"),
    path('item/item_update/<slug:id>/', views.item, name="itemUpdate"),
    path('item/item_delete/<slug:id>/', views.itemDelete, name="itemDelete"),


    # =========================== CATEGORY ===========================
    path('item/category', views.categoryIndex, name="categoryIndex"),
    path('item/category/category_create',
         views.category, name="categoryCreate"),
    path('item/category/category_update/<slug:id>/',
         views.category, name="categoryUpdate"),
    path('item/category/category_delete/<slug:id>/',
         views.categoryDelete, name="categoryDelete"),

    # -------------------- Inbound --------------------------
    path('inbound/', views.main_inbound, name="inboundIndex"),
    path('inbound/add_inbound', views.inbound, name="add_inbound"),
    path('inbound/delete_inbound/<slug:id>/',
         views.delete_inbound, name="delete_inbound"),
    path('inbound/view_inbound/<slug:id>/',
         views.view_inbound, name="view_inbound"),
    # path('inbound/confirm/',
    #      views.confirm, name="confirm"),


    # -------------------- Itemdata --------------------------
    path('inbound/add_inbounddata', views.inbound_data, name="add_inbounddata"),
    path('inbound/update_inbounddata/<slug:id>/',
         views.inbound_data, name="update_inbounddata"),
    path('inbound/delete_inbounddata/<slug:id>/',
         views.delete_inbounddata, name="delete_inbounddata"),

    # -------------------- PDFInbound --------------------------
    #path('inbound/<int:pk>/', views.PdfInbound.as_view(),),
    path('inbound/<slug:pk>/', views.PdfInbound.as_view(),),

    # --------------------- SUPPLIER ------------------
    path('supplier/', views.list_supplier, name="list_supplier"),
    path('supplier/add_supplier/', views.supplier, name="add_supplier"),
    path('supplier/update_supplier/<slug:id>/',
         views.supplier, name="update_supplier"),
    path('supplier/delete/<slug:id>/',
         views.supplier_delete, name="delete_supplier"),
    path('supplier/detail/<slug:id>/',
         views.supplier_detail, name="detail_supplier"),

    # =========================== SUBCATEGORY =========================

    path('item/category/subcategory/view/<slug:id>/',
         views.subcategoryIndex, name="subcategoryIndex"),
    path('item/category/subcategory/subcategory_create/',
         views.subcategory, name="subcategoryCreate"),
    path('item/category/subcategory/subcategory_update/<slug:id>/',
         views.subcategory, name="subcategoryUpdate"),
    path('item/category/subcategory/subcategory_delete/<slug:id>/',
         views.subcategoryDelete, name="subcategoryDelete"),

]
