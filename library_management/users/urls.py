from django.urls import path, include

from django.views.generic.base import TemplateView

from library_management.users import views

urlpatterns = [
    path('change-password/', views.change_password, name='change_password'),
    path('user-profile/<int:pk>/update', views.user_profile_update, name='user_profile_update'),
    path('user-profile/photo/<int:pk>/update', views.user_profile_photo_update, name='user_profile_photo_update'),
]
