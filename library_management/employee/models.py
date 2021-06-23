from django.db import models
from django.utils.translation import gettext as _

from library_management.core.models import Library
from library_management.users.models import CustomUser


class Employee(models.Model):
    custom_user = models.ForeignKey(CustomUser, verbose_name=_("Пользователь"), on_delete=models.CASCADE)
    library = models.ForeignKey(Library, verbose_name=_("Библиотека"), on_delete=models.CASCADE)
    position = models.CharField(verbose_name=_("Должность"), max_length=255, null=True)
    phone_number = models.CharField(verbose_name=_("Номер телефона"), max_length=20, null=True)

    def __str__(self):
        return f'{self.custom_user.email}'
