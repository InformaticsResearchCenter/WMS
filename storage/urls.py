from . import views
from django.urls import path

urlpatterns = [
    path('', views.scanner, name="index"),
    path('rack/add_rack', views.rack, name="add_rack"),
    path('rack/', views.main_rack, name="rack"),
    path('rack/view_rack/<slug:id>/', views.view_rack, name="view_rack"),
    path('rack/delete_rack/<slug:id>/', views.delete_rack, name="delete_rack"),

    # -------------------- PDFRack --------------------------
    path('rack/<slug:pk>/', views.PdfRack.as_view(),),
]
