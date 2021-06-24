import re
from datetime import date
from io import BytesIO

import qrcode
import qrcode.image.svg
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, DeleteView

from library_management.core.decorators import superuser_required, admin_or_emp_required, student_required
from library_management.core.forms import CountryForm, RegionForm, DistrictForm, LibraryForm, EmployeeCreateForm, \
    CategoryForm, BookForm
from library_management.core.models import Country, Region, District, Library, Category, Book, BookInstance
from library_management.employee.models import Employee, Student, StudentBooks
from library_management.users.models import CustomUser


def homepage(request):
    return render(request, 'core/default_homepage.html', {'title': 'Главная страница'})


@superuser_required
def country_list(request):

    countries = Country.objects.all().order_by('name')

    return render(request, 'core/country/country_list.html', {'countries': countries, 'title': 'Список стран'})


@superuser_required
def country_create(request):
    if request.method == "POST":
        form = CountryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('country_list')
    else:
        form = CountryForm()
    return render(request, 'core/country/country_form.html', {'form': form, 'title': 'Добавление страны'})


@superuser_required
def country_update(request, pk):
    country = Country.objects.get(id=pk)
    if request.method == "POST":
        form = CountryForm(request.POST, instance=country)
        if form.is_valid():
            form.save()
            return redirect('country_list')
    else:
        form = CountryForm(instance=country)
    return render(request, 'core/country/country_form.html', {'form': form, 'title': 'Изменение страны'})


@superuser_required
def country_delete(request, pk):
    country = Country.objects.get(id=pk)
    country.delete()

    return redirect('country_list')


@superuser_required
def region_list(request):

    regions = Region.objects.all().order_by('name')

    return render(request, 'core/region/region_list.html', {'regions': regions, 'title': 'Список областей'})


@superuser_required
def region_create(request):
    if request.method == "POST":
        form = RegionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('region_list')
    else:
        form = RegionForm()
    return render(request, 'core/region/region_form.html', {'form': form, 'title': 'Добавление области'})


@superuser_required
def region_update(request, pk):
    region = Region.objects.get(id=pk)
    if request.method == "POST":
        form = RegionForm(request.POST, instance=region)
        if form.is_valid():
            form.save()
            return redirect('region_list')
    else:
        form = RegionForm(instance=region)
    return render(request, 'core/region/region_form.html', {'form': form, 'title': 'Изменение области'})


@superuser_required
def region_delete(request, pk):
    region = Region.objects.get(id=pk)
    region.delete()

    return redirect('region_list')


@superuser_required
def district_list(request):

    districts = District.objects.all().order_by('name')

    return render(request, 'core/district/district_list.html', {'districts': districts, 'title': 'Список районов'})


@superuser_required
def district_create(request):
    if request.method == "POST":
        form = DistrictForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('district_list')
    else:
        form = DistrictForm()
    return render(request, 'core/district/district_form.html', {'form': form, 'title': 'Добавление района'})


@superuser_required
def district_update(request, pk):
    district = District.objects.get(id=pk)
    if request.method == "POST":
        form = DistrictForm(request.POST, instance=district)
        if form.is_valid():
            form.save()
            return redirect('district_list')
    else:
        form = DistrictForm(instance=district)
    return render(request, 'core/district/district_form.html', {'form': form, 'title': 'Изменение района'})


@superuser_required
def district_delete(request, pk):
    district = District.objects.get(id=pk)
    district.delete()

    return redirect('district_list')


@superuser_required
def library_list(request):

    libraries = Library.objects.all().order_by('name')

    return render(request, 'core/library/library_list.html', {'libraries': libraries, 'title': 'Список библиотек'})


@superuser_required
def library_create(request):
    if request.method == "POST":
        form = LibraryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('library_list')
    else:
        form = LibraryForm()
    return render(request, 'core/library/library_form.html', {'form': form, 'title': 'Добавление библиотеки'})


@superuser_required
def library_update(request, pk):
    library = Library.objects.get(id=pk)
    if request.method == "POST":
        form = LibraryForm(request.POST, instance=library)
        if form.is_valid():
            form.save()
            return redirect('library_list')
    else:
        form = LibraryForm(instance=library)
    return render(request, 'core/library/library_form.html', {'form': form, 'title': 'Изменение библиотеки'})


@superuser_required
def library_delete(request, pk):
    library = Library.objects.get(id=pk)
    library.delete()

    return redirect('library_list')


@superuser_required
def library_user_list(request, pk):

    library = Library.objects.get(id=pk)
    library_users = Employee.objects.filter(library=library)

    return render(request, 'core/library/library_user_list.html', {'library': library,
                                                                   'library_users': library_users,
                                                                   'title': 'Список сотрудников библиотеки'})


@method_decorator([login_required, superuser_required], name='dispatch')
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
        library = Library.objects.get(id=self.kwargs['fk'])
        form.library = library
        user = form.save()
        return redirect('library_user_list', self.kwargs['fk'])


@superuser_required
def employee_delete(request, pk):
    employee = Employee.objects.get(id=pk)
    library = employee.library
    employee.custom_user.delete()
    employee.delete()

    return redirect('library_user_list', library.pk)


def category_list(request):

    categories = Category.objects.all().order_by('name')

    return render(request, 'core/category/category_list.html', {'categories': categories, 'title': 'Список жанров'})


def category_create(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'core/category/category_form.html', {'form': form, 'title': 'Добавление жанра'})


def category_update(request, pk):
    category = Category.objects.get(id=pk)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'core/category/category_form.html', {'form': form, 'title': 'Изменение жанра'})


def category_delete(request, pk):
    category = Category.objects.get(id=pk)
    category.delete()

    return redirect('category_list')


@admin_or_emp_required
def book_list(request):
    custom_user = CustomUser.objects.get(id=request.user.id)
    employee = Employee.objects.get(custom_user=custom_user)
    books = Book.objects.filter(library=employee.library)

    return render(request, 'core/book/book_list.html', {'books': books, 'title': 'Список книг'})


@admin_or_emp_required
def book_create(request):
    custom_user = CustomUser.objects.get(id=request.user.id)
    employee = Employee.objects.get(custom_user=custom_user)
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.library = employee.library
            obj.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'core/book/book_form.html', {'form': form, 'title': 'Добавление книги'})


@admin_or_emp_required
def book_update(request, pk):
    book = Book.objects.get(id=pk)
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'core/book/book_form.html', {'form': form, 'title': 'Изменение книги'})


@admin_or_emp_required
def book_delete(request, pk):
    book = Book.objects.get(id=pk)
    book_instances = BookInstance.objects.filter(book=book)

    for book_instance in book_instances:
        book_instance.delete()

    book.delete()

    return redirect('book_list')


@admin_or_emp_required
def search_book(request):
    custom_user = CustomUser.objects.get(id=request.user.id)
    employee = Employee.objects.get(custom_user=custom_user)

    query_string = ''
    found_entries = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']

        entry_query = get_query(query_string, ['name', 'description', 'author'])

        books = Book.objects.filter(entry_query).filter(library=employee.library)

    return render(request, 'core/book/book_list.html', locals())


@admin_or_emp_required
def book_details(request, pk):
    book = Book.objects.get(id=pk)
    book_instances = BookInstance.objects.filter(book=book)

    return render(request, 'core/book/book_details.html', {'book_instances': book_instances,
                                                           'book': book,
                                                           'title': 'Информация о книге'})


@admin_or_emp_required
def book_add_instance(request, pk):
    book = Book.objects.get(id=pk)

    book_instance = BookInstance.objects.create(book=book, is_free=True)
    book_instance.qr_code = generate_qr(request, book_instance.id)
    book_instance.save()

    return redirect('book_details', book.id)


def generate_qr(request, pk):
    factory = qrcode.image.svg.SvgImage
    img = qrcode.make(pk, image_factory=factory, box_size=15)
    stream = BytesIO()
    img.save(stream)
    return stream.getvalue().decode()


def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.

    '''
    query = None # Query to search for every search term
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query

def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:

        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']

    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]


@student_required
def book_list_student(request):
    custom_user = CustomUser.objects.get(id=request.user.id)
    student = Student.objects.get(custom_user=custom_user)
    books = StudentBooks.objects.filter(student=student)

    return render(request, 'core/book/student_book_list.html', {'books': books, 'title': 'Список моих книг'})
