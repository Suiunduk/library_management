import os

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.forms import widgets
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CustomUserCreationForm, CustomUserForm, CustomUserProfilePhotoForm
from .models import CustomUser


class SignUp(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'users/signup.html'

    def get_form(self, **kwargs):
        form = super(SignUp, self).get_form()
        form.fields['date_of_birth'].widget = widgets.DateInput(
            attrs={'type': 'date'})
        return form


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Ваш пароль был успешно изменён!')
            return redirect('change_password')
        else:
            messages.error(request, 'Пожалуйста введите правильные данные')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/change_password.html', {
        'form': form
    })


# def user_profile(request):
#     user = request.user
#     customUser = CustomUser.objects.get(pk=user.pk)
#     if customUser.user_type == 'student_applicant':
#         return student_applicant_profile(request)
#
#     elif customUser.user_type == 'super_user':
#         return super_user_profile(request)
#
#     return render(request, 'users/user_profile.html', {'user': user})


def user_profile_update(request, pk):
    # user = request.user
    custom_user = get_object_or_404(CustomUser, pk=pk)
    data = dict()

    if request.method == 'POST':
        form = CustomUserForm(request.POST, instance=custom_user)
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            data['html_user_profile'] = render_to_string('users/partial_user_profile_info.html', {'user': request.user})
        else:
            data['form_is_valid'] = False
    else:
        form = CustomUserForm(instance=custom_user)

    context = {'form': form}
    data['html_form'] = render_to_string('users/partial_user_profile_update.html', context, request=request)
    return JsonResponse(data)


def user_profile_photo_update(request, pk):
    custom_user = get_object_or_404(CustomUser, pk=pk)
    file = custom_user.profile_photo
    data = dict()

    if request.method == 'POST':
        form = CustomUserProfilePhotoForm(request.POST, request.FILES, instance=custom_user)
        if form.is_valid():
            form.save()
            if file:
                os.remove(file.path)
            data['form_is_valid'] = True
            data['html_user_profile'] = render_to_string('users/partial_user_profile_info.html', {'user': request.user})
        else:
            data['form_is_valid'] = False
    else:
        form = CustomUserProfilePhotoForm(instance=custom_user)

    context = {'form': form}
    data['html_form'] = render_to_string('users/partial_user_profile_photo_update.html', context, request=request)

    return JsonResponse(data)
