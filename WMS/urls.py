from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [

path('', views.index, name="homepage"),
    path('app/', include('wmsApp.urls')),
    path('admin/', include('wmsAdmin.urls')),
    path('group/', include('wmsGroup.urls')),
    path('storage/', include('wmsStorage.urls')),
    path('inbound/', include('wmsInbound.urls')),
    path('outbound/', include('wmsOutbound.urls')),

    # path('user/', views.usermanagement, name="user"),
    # path('add_user/', views.userdata, name="add_user"),
    # path('update_user/<slug:id>/',
    #      views.userdata, name="update_user"),
    # path('user/delete_user/<slug:id>/', views.delete_user, name="delete_user"),
    # path('category/', include('category.urls')),
    # path('storage/', include('storage.urls')),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
