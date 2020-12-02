from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


from . import views

urlpatterns = [
    path('', views.borrowIndex, name="borrowIndex"),
    path('borrow_view/<slug:id>/', views.borrowView, name="borrowView"),
    path('borrow_create/', views.borrow, name="borrowCreate"),
    path('borrow_update/<slug:id>/',
         views.borrow, name="borrowUpdate"),
    path('borrow_delete/<slug:id>/',
         views.borrowDelete, name="borrowDelete"),
    path('borrowdata_create/', views.borrowdata, name="borrowdataCreate"),
    path('borrowdata_confirm/', views.borrowdataConfirm, name="borrowdataConfirm"),
    path('borrowdata_return/', views.borrowdataReturn, name="borrowdataReturn"),
    path('borrowdata_update/<slug:id>/',
         views.borrowdata, name="borrowdataUpdate"),
    path('borrowdata_delete/<slug:id>/',
         views.borrowdataDelete, name="borrowdataDelete"),

    path('<slug:pk>/', views.PdfBorrow.as_view(),),
]
