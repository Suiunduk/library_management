from django import forms

from library_management.core.models import Country, Region, District, Library


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
