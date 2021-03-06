from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views


urlpatterns = [
    path('', views.main_outbound, name="outbound"),
    path('add_outbound', views.outbound, name="add_outbound"),
    path('view_outbound/<slug:id>/', views.view_outbound, name="view_outbound"),
    path('delete_outbound/<slug:id>/',
         views.delete_outbound, name="delete_outbound"),
    path('add_outbounddata/', views.outbounddata, name="add_outbounddata"),
    path('delete_outbounddata/<slug:id>/',
         views.delete_outbounddata, name="delete_outbounddata"),
    path('confirm/', views.confirm, name='confirm_outbound'),
    path('update_outbounddata/<slug:id>/',
         views.outbounddata, name="update_outbounddata"),
    # -------------------- PDFOutbound --------------------------
    path('<slug:pk>/', views.PdfOutbound.as_view(),),


    path('customer', views.main_customer, name="customer"),
    path('add_customer', views.customer, name="add_customer"),
    path('delete_customer/<slug:id>/',
         views.delete_customer, name="delete_customer"),
    path('update_customer/<slug:id>/',
         views.customer, name="update_customer"),
    path('customer/detail/<slug:id>/',
         views.customer_detail, name="detail_customer"),          
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)