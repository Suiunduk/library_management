from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from library_management.core.models import Country, Region, District, Library, Category, Book, BookInstance
from library_management.employee.models import Employee, Student
from library_management.users.models import CustomUser


class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = "__all__"


class RegionForm(forms.ModelForm):
    class Meta:
        model = Region
        fields = "__all__"


class DistrictForm(forms.ModelForm):
    class Meta:
        model = District
        fields = "__all__"


class LibraryForm(forms.ModelForm):
    class Meta:
        model = Library
        fields = "__all__"


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('name', 'description', 'author', 'photo', 'category')


class EmployeeCreateForm(UserCreationForm):
    is_admin = forms.BooleanField(label='Администратор библиотеки', required=False)
    position = forms.CharField(label='Должность', max_length=255)
    phone_number = forms.CharField(label='Номер телефона', max_length=255)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'password1', 'password2', 'last_name', 'first_name', 'middle_name', 'date_of_birth',
                  'gender', 'profile_photo')

    @transaction.atomic
    def save(self):
        user = super(EmployeeCreateForm, self).save(commit=False)
        if self.cleaned_data.get('is_admin'):
            user.user_type = 'library_admin'
        else:
            user.user_type = 'employee'
        user.save()
        employee = Employee.objects.create(custom_user=user,
                                           position=self.cleaned_data.get('position'),
                                           phone_number=self.cleaned_data.get('phone_number'),
                                           library=self.library)
        return user


class StudentCreateForm(UserCreationForm):
    phone_number = forms.CharField(label='Номер телефона', max_length=255)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'password1', 'password2', 'last_name', 'first_name', 'middle_name', 'date_of_birth',
                  'gender', 'profile_photo')

    @transaction.atomic
    def save(self):
        user = super(StudentCreateForm, self).save(commit=False)
        user.user_type = 'student'
        user.save()
        student = Student.objects.create(custom_user=user,
                                         phone_number=self.cleaned_data.get('phone_number'),
                                         library=self.library)
        return user

