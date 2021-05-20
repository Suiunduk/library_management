from datetime import date

from django.shortcuts import render, redirect

# Create your views here.
from library_management.core.decorators import superuser_required
from library_management.core.forms import CountryForm, RegionForm, DistrictForm, LibraryForm
from library_management.core.models import Country, Region, District, Library


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
