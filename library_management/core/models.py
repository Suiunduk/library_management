from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _

NOTIFICATION_TYPE_CHOICES = (
    ('success', _("Успешное уведомление")),
    ('default', _("Обычное уведомление")),
    ('danger', _("Критическое уведомление")),
    ('info', _("Информационное уведомление")),
)


class Country(models.Model):
    name = models.CharField(verbose_name=_("Название"), max_length=255, unique=True)
    longitude = models.DecimalField(verbose_name=_("Долгота"), null=True, max_digits=9, decimal_places=6, default=0)
    latitude = models.DecimalField(verbose_name=_("Широта"), null=True, max_digits=9, decimal_places=6, default=0)

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('country_list')


class Region(models.Model):
    name = models.CharField(verbose_name=_("Наименование"), max_length=255, unique=True)
    country = models.ForeignKey(Country, verbose_name=_("Страна"), on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('region_list')


class District(models.Model):
    name = models.CharField(verbose_name=_("Наименование"), max_length=255, unique=True)
    region = models.ForeignKey(Region, verbose_name=_("Область"), on_delete=models.DO_NOTHING)
    is_city = models.BooleanField(verbose_name=_("Город"), default=False)

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('district_list')


class Library(models.Model):
    name = models.CharField(verbose_name=_("Наименование"), max_length=255)
    district = models.ForeignKey(District, verbose_name=_("Район"), on_delete=models.DO_NOTHING)
    address = models.CharField(verbose_name=_("Адрес"), max_length=255)

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('Library_list')
