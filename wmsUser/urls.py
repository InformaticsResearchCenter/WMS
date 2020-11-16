from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views
urlpatterns = [
    path('', views.index, name="userIndex"),
    path('create', views.create, name="userCreate"),
    path('update', views.update, name="userUpdate"),
    path('delete', views.delete, name="userDelete"),
]
