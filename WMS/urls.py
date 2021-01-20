from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [

path('', views.index, name="homepage"),
path('admin/', include('wmsAdmin.urls')),
path('group/', include('wmsGroup.urls')),
path('app/', include('wmsApp.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
