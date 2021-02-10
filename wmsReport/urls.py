from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.reportIndex, name="report"),
    path('<status>', views.reportDetail, name="reportdetail"),
    path('log/', views.log, name="reportlog")
]
