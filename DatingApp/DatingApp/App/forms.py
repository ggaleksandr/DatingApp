from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import AppUser


class AppUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = AppUser
        widgets = {
            'password': forms.PasswordInput(),
        }
        fields = ('profile_pic', 'gender', 'first_name', 'last_name', 'email', 'password')


class AppUserChangeForm(UserChangeForm):
    class Meta:
        model = AppUser
        fields = ('profile_pic', 'gender', 'first_name', 'last_name', 'email', 'password')