from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    # =========================== CATEGORY ===========================
    path('item/', views.itemIndex, name="itemIndex"),
    path('item/category', views.categoryIndex, name="categoryIndex"),
    path('item/category/category_create',
         views.category, name="categoryCreate"),
    path('item/category/category_update/<slug:id>/',
         views.category, name="categoryUpdate"),
    path('item/category/category_delete/<slug:id>/',
         views.category_delete, name="categoryDelete"),

<<<<<<< HEAD
    # -------------------- Inbound --------------------------
    # path('inbound/', views.main_inbound, name="inboundIndex"),

    # --------------------- SUPPLIER ------------------
    path('supplier/', views.list_supplier, name="list_supplier"),
    path('supplier/add_supplier/', views.supplier, name="add_supplier"),
    path('update_supplier/<slug:id>/', views.supplier, name="update_supplier"),
    path('supplier/delete/<slug:id>/',
         views.supplier_delete, name="delete_supplier"),
    path('supplier/detail/<slug:id>/',
         views.supplier_detail, name="detail_supplier"),
=======
    # =========================== SUBCATEGORY =========================

    path('item/category/subcategory/view/<slug:id>/',
         views.subcategoryIndex, name="subcategoryIndex"),
    path('item/category/subcategory/subcategory_create/',
         views.subcategory, name="subcategoryCreate"),
    path('item/category/subcategory/subcategory_update/<slug:id>/',
         views.subcategory, name="subcategoryUpdate"),
    path('item/category/subcategory/subcategory_delete/<slug:id>/',
         views.subcategoryDelete, name="subcategoryDelete"),
>>>>>>> 3d75e840509d729c04323b70b1a17b7606074bcf
]
