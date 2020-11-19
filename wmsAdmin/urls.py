from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.index, name="adminIndex"),
    path('login', views.login, name="adminLogin"),
    path('logout', views.logout, name="adminLogout"),
    path('limit/<slug:id>/', views.limit, name="limit"),
    path('deactive/<slug:id>/', views.deactive, name="deactive"),
]
