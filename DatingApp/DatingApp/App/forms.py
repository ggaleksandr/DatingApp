from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import AppUser


class AppUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = AppUser
        fields = ('profile_pic', 'gender', 'first_name', 'last_name', 'email',)


class AppUserChangeForm(UserChangeForm):
    class Meta:
        model = AppUser
        fields = ('profile_pic', 'gender', 'first_name', 'last_name', 'email',)