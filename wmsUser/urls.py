from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.index, name="userIndex"),
    path('user_create', views.user, name="userCreate"),
    path('user_update/<slug:id>/', views.user, name="userUpdate"),
    path('user_delete/<slug:id>/', views.user_delete, name="userDelete"),
]
