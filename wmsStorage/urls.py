from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('item/', views.getItemData, name="itemdata"),
    path('scanner/', views.scanner, name="scanner"),
    path('scanner/getScannerData', views.getScannerData, name="scannerdata"),
    path('scanner/checkOutbound', views.getOutboundData, name="outbounddata"),
    path('scanner/checkReturn', views.getReturnData, name="returndata"),
    path('scanner/checkBorrow', views.getBorrowData, name="borrowdata"),
    path('scanner/put', views.put, name="put"),
    path('scanner/out', views.out, name="out"),
    path('scanner/move', views.move, name="move"),
    path('scanner/borrow', views.borrow, name="borrow"),
    path('scanner/return', views.retur, name="return"),


    # ======================================= RACK =============================================
    path('rack/', views.rackIndex, name="rackIndex"),
    path('rack/rack_create', views.rack, name="rackCreate"),
    path('rack/rack_delete/<slug:id>/', views.rackDelete, name="rackDelete"),
    path('rack/rack_view/<slug:id>/', views.rackView, name="rackView"),

    path('rack/<slug:pk>/', views.PdfRack.as_view(),),
]
