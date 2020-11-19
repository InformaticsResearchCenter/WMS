from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('item/', views.itemIndex, name="itemIndex"),
    path('item/category', views.categoryIndex, name="categoryIndex"),
    path('item/category/category_create',
         views.category, name="categoryCreate"),
    path('item/category/category_update/<slug:id>/',
         views.category, name="categoryUpdate"),
    path('item/category/category_delete/<slug:id>/',
         views.category_delete, name="categoryDelete"),
]
