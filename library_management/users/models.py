from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _

USER_TYPE_CHOICES = (
    ('super_user', _("Администратор")),
    ('library_admin', _("Администратор библиотеки")),
    ('employee', _("Сотрудник библиотеки")),
    ('student', _("Студент")),
)
GENDERS = (
    ('2', _("Мужской")),
    ('1', _("Женский")),
)


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('Email обязательное поле'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(verbose_name=_('E-mail'), unique=True)
    first_name = models.CharField(verbose_name=_("Имя"), max_length=255)
    last_name = models.CharField(verbose_name=_("Фамилия"), max_length=255)
    middle_name = models.CharField(verbose_name=_("Отчество"), max_length=255, blank=True)
    date_of_birth = models.DateField(verbose_name=_("Дата рождения"), default=timezone.now)
    gender = models.CharField(verbose_name=_("Пол"), choices=GENDERS, max_length=255, default='male')
    profile_photo = models.ImageField(verbose_name=_("Фотография профиля"), blank=True, null=True,
                                      upload_to='users/profile_photos')
    user_type = models.CharField(verbose_name=_("Тип пользователя"), choices=USER_TYPE_CHOICES, default="super_user",
                                 max_length=255)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def delete(self, *args, **kwargs):
        self.profile_photo.delete()
        return super(self.__class__, self).delete(*args, **kwargs)