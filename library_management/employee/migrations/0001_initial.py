# Generated by Django 3.2.3 on 2021-06-23 12:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0002_library'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(max_length=255, null=True, verbose_name='Должность')),
                ('phone_number', models.CharField(max_length=20, null=True, verbose_name='Номер телефона')),
                ('custom_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
                ('library', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.library', verbose_name='Библиотека')),
            ],
        ),
    ]
