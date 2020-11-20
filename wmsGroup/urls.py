from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.index, name="groupIndex"),
    path('login/', views.login, name="groupLogin"),
    path('register/', views.register, name="groupRegister"),
    path('logout/', views.logout, name="groupLogout"),
]
