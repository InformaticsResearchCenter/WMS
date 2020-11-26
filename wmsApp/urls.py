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
    path('inbound/', include('wmsInbound.urls')),
    path('outbound/', include('wmsOutbound.urls')),
    path('storage/', include('wmsStorage.urls')),
    path('borrow/', include('wmsBorrow.urls')),
    
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
