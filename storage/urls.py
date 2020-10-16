from . import views
from django.urls import path

urlpatterns = [
    path('', views.scanner, name="storage"),
    path('put/', views.put, name="put"),
    # path('move/', views.move, name="move"),
    # path('out/', views.out, name="out")
]
