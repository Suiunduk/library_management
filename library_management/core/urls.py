from django.conf.urls import url
from django.urls import path

from library_management.core import views
from library_management.core.views import EmployeeCreateView

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

    path('category/list', views.category_list, name='category_list'),
    path('category/create', views.category_create, name='category_create'),
    path('category/update/<int:pk>', views.category_update, name='category_update'),
    path('category/delete/<int:pk>', views.category_delete, name='category_delete'),


    path('library/user/list/<int:pk>', views.library_user_list, name='library_user_list'),
    path('library/user/create/<int:fk>', EmployeeCreateView.as_view(), name='library_user_create'),
    path('library/user/delete/<int:pk>/', views.employee_delete, name='library_user_delete'),

    path('book/list', views.book_list, name='book_list'),
    path('book/create', views.book_create, name='book_create'),
    path('book/update/<int:pk>/', views.book_update, name='book_update'),
    path('book/delete/<int:pk>/', views.book_delete, name='book_delete'),
    path('book/details/<int:pk>/', views.book_details, name='book_details'),
    path('book/add_instance/<int:pk>/', views.book_add_instance, name='book_add_instance'),

    url(r'^book/list/search_b/', views.search_book, name="search_b"),
]
