from . import views
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


from . import views

urlpatterns = [
    path('costumer/', views.costumerReturnIndex, name="costumerReturnIndex"),
    path('costumer/costumerReturn_create',
         views.costumerReturn, name="costumerReturnCreate"),
    path('costumer/costumerReturn_confirm',
         views.costumerReturnConfirm, name="costumerReturnConfirm"),
    path('costumer/costumerReturn_view/<slug:id>',
         views.costumerReturnDataIndex, name="costumerReturndataIndex"),
    path('costumer/costumerReturn_delete/<slug:id>',
         views.costumerReturnDelete, name="costumerReturnDelete"),
    path('costumer/costumerReturndata_create',
         views.costumerReturndata, name="costumerReturndataCreate"),
    path('costumer/costumerReturndata_delete/<slug:id>',
         views.costumerReturndataDelete, name="costumerReturndataDelete"),
    path('costumer/costumerReturndata_update/<slug:id>',
         views.costumerReturndata, name="costumerReturndataUpdate"),

    # -------------------------------- Supplier Return ---------------------------
    path('supplier/', views.supplierReturnIndex, name="supplierReturnIndex"),
    path('supplier/supplierReturn_create',
         views.supplierReturn, name="supplierReturnCreate"),
    path('supplier/supplierReturn_view/<slug:id>',
         views.supplierReturnDataIndex, name="supplierReturndataIndex"),
    path('supplier/supplierReturn_delete/<slug:id>',
         views.supplierReturnDelete, name="supplierReturnDelete"),
    path('supplier/supplierReturn_confirm',
         views.supplierReturnConfirm, name="supplierReturnConfirm"),
    path('supplier/supplierReturndata_create',
         views.supplierReturndata, name="supplierReturndataCreate"),
    path('supplier/supplierReturndata_delete/<slug:id>',
         views.supplierReturndataDelete, name="supplierReturndataDelete"),
    # -------------------- PDFInbound --------------------------
    path('supplier/<slug:pk>/', views.PdfSupplierReturn.as_view(),),
    path('costumer/<slug:pk>/', views.PdfCostumerReturn.as_view(),),
]
