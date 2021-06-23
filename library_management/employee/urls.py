from django.urls import path

from library_management.employee import views
from library_management.employee.views import EmployeeCreateView

urlpatterns = [
    path('employee/list', views.employee_list, name='employee_list'),
    path('employee/user/create', EmployeeCreateView.as_view(), name='employee_create'),
    path('employee/user/delete/<int:pk>', views.employee_delete, name='employee_delete'),
]