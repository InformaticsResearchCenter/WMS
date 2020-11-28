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
]
