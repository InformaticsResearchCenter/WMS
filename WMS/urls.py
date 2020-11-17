"""WMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('user/', include('wmsUser.urls')),
    path('admin/', include('wmsAdmin.urls')),
    # path('user/', views.usermanagement, name="user"),
    # path('add_user/', views.userdata, name="add_user"),
    # path('update_user/<slug:id>/',
    #      views.userdata, name="update_user"),
    # path('user/delete_user/<slug:id>/', views.delete_user, name="delete_user"),
    # path('category/', include('category.urls')),
    # path('storage/', include('storage.urls')),
    # path('outbound/', include('outbound.urls')),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
