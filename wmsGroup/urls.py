from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views
from .views import VerificationView, ResetPassword

urlpatterns = [
    path('', views.index, name="groupIndex"),
    # path('login/', views.login, name="groupLogin"),
    path('register/', views.register, name="groupRegister"),
    path('reset/', views.resetPassword, name="groupReset"),
    path('logout/', views.logout, name="groupLogout"),
    path('activate/<email>/<token>', VerificationView.as_view(), name="activate"),
    path('reset/<email>/<token>', ResetPassword.as_view(), name="reset"),



    path('usergroup/', views.edit_usergroup, name="edit_userGroup"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
