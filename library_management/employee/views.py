from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import CreateView

from library_management.core.decorators import library_admin_required, admin_or_emp_required
from library_management.core.forms import EmployeeCreateForm, StudentCreateForm
from library_management.core.models import Library
from library_management.employee.models import Employee, Student
from library_management.users.models import CustomUser


@library_admin_required
def employee_list(request):
    custom_user = CustomUser.objects.get(id=request.user.id)
    employee = Employee.objects.get(custom_user=custom_user)
    employees = Employee.objects.filter(library=employee.library).exclude(custom_user=custom_user)

    return render(request, 'employee/employee_list.html', {'employees': employees, 'title': 'Список сотрудников'})


@method_decorator([login_required, library_admin_required], name='dispatch')
class EmployeeCreateView(SuccessMessageMixin, CreateView):
    model = CustomUser
    form_class = EmployeeCreateForm
    template_name = 'core/library/employee_form.html'
    success_message = "Новый сотрудник успешно добавлен"

    def get_context_data(self, **kwargs):
            kwargs['user_type'] = 'employee'
            return super().get_context_data(**kwargs)

    def get_form(self, **kwargs):
        form = super(EmployeeCreateView, self).get_form()
        return form

    def form_valid(self, form):
        custom_user = CustomUser.objects.get(id=self.request.user.id)
        employee = Employee.objects.get(custom_user=custom_user)
        form.library = employee.library
        user = form.save()
        return redirect('employee_list')


@library_admin_required
def employee_delete(request, pk):
    employee = Employee.objects.get(id=pk)
    employee.custom_user.delete()
    employee.delete()

    return redirect('employee_list')


@admin_or_emp_required
def student_list(request):
    custom_user = CustomUser.objects.get(id=request.user.id)
    employee = Employee.objects.get(custom_user=custom_user)
    students = Student.objects.filter(library=employee.library)

    return render(request, 'student/student_list.html', {'students': students, 'title': 'Список студентов'})


@method_decorator([login_required, admin_or_emp_required], name='dispatch')
class StudentCreateView(SuccessMessageMixin, CreateView):
    model = CustomUser
    form_class = StudentCreateForm
    template_name = 'core/library/student_form.html'
    success_message = "Новый студент успешно добавлен"

    def get_context_data(self, **kwargs):
            kwargs['user_type'] = 'student'
            return super().get_context_data(**kwargs)

    def get_form(self, **kwargs):
        form = super(StudentCreateView, self).get_form()
        return form

    def form_valid(self, form):
        custom_user = CustomUser.objects.get(id=self.request.user.id)
        employee = Employee.objects.get(custom_user=custom_user)
        form.library = employee.library
        user = form.save()
        return redirect('student_list')
