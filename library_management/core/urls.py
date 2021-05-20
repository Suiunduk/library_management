from django.urls import path

from library_management.core import views

urlpatterns = [
    # Homepage url
    path('', views.homepage, name='homepage'),

    path('country/list', views.country_list, name='country_list'),
    path('country/create', views.country_create, name='country_create'),
    path('country/update/<int:pk>', views.country_update, name='country_update'),
    path('country/delete/<int:pk>', views.country_delete, name='country_delete'),

    path('region/list', views.region_list, name='region_list'),
    path('region/create', views.region_create, name='region_create'),
    path('region/update/<int:pk>', views.region_update, name='region_update'),
    path('region/delete/<int:pk>', views.region_delete, name='region_delete'),

    path('district/list', views.district_list, name='district_list'),
    path('district/create', views.district_create, name='district_create'),
    path('district/update/<int:pk>', views.district_update, name='district_update'),
    path('district/delete/<int:pk>', views.district_delete, name='district_delete'),

    path('library/list', views.library_list, name='library_list'),
    path('library/create', views.library_create, name='library_create'),
    path('library/update/<int:pk>', views.library_update, name='library_update'),
    path('library/delete/<int:pk>', views.library_delete, name='library_delete'),
]
