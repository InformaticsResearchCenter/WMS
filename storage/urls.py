from . import views
from django.urls import path

urlpatterns = [
    # path('', views.scanner, name="storage"),
    # path('move/', views.move, name="move"),
    # path('out/', views.out, name="out")
    path('', views.index, name="index"),
    # path('index', views.index, name="index"),
    path('getScannerData', views.getScannerData, name="getScannerData"),
    path('checkItem', views.checkItem, name="checkItem"),
    path('put/', views.put, name="put"),    
    path('testing/', views.testing, name="testing"),    
    path('out/', views.out, name="out"),    
    path('checkOutbound/', views.checkOutbound, name="checkOutbound"),    
    path('move/', views.move, name="move"),    
    path('rack/add_rack', views.rack, name="add_rack"),
    path('rack/', views.main_rack, name="rack"),
    path('rack/view_rack/<slug:id>/', views.view_rack, name="view_rack"),
    path('rack/delete_rack/<slug:id>/', views.delete_rack, name="delete_rack"),

    # -------------------- PDFRack --------------------------
    path('rack/<slug:pk>/', views.PdfRack.as_view(),),
]
