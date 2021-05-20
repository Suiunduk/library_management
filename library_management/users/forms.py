from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.files.images import get_image_dimensions

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email', 'last_name', 'first_name', 'middle_name', 'date_of_birth', 'gender', 'profile_photo',)


class CustomUserForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ('email', 'last_name', 'first_name', 'middle_name', 'date_of_birth', 'gender',)


class CustomUserProfilePhotoForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ('profile_photo',)

    def clean_avatar(self):
        avatar = self.cleaned_data['profile_photo']

        try:
            w, h = get_image_dimensions(avatar)

            # validate dimensions
            max_width = max_height = 500
            if w > max_width or h > max_height:
                raise forms.ValidationError(
                    u'Пожалуйста выберите избражение с разнешением '
                    '%s x %s пикселей или меньше.' % (max_width, max_height))

            # validate content type
            main, sub = avatar.content_type.split('/')
            if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
                raise forms.ValidationError(u'Пожалуйста используйте изображение в формате JPEG, '
                                            'GIF или PNG.')

            # validate file size
            if len(avatar) > (20 * 1024):
                raise forms.ValidationError(
                    u'Размер файла слишком большой')

        except AttributeError:
            """
            Handles case when we are updating the user profile
            and do not supply a new avatar
            """
            pass

        return avatar
