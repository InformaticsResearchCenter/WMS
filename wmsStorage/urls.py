from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    # ======================================= RACK =============================================
    path('rack/', views.rackIndex, name="rackIndex"),
    path('rack/rack_create', views.rack, name="rackCreate"),
    path('rack/rack_delete/<slug:id>/', views.rackDelete, name="rackDelete"),
    path('rack/rack_view/<slug:id>/', views.rackView, name="rackView"),
]
