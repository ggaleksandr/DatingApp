from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import AppUserCreationForm, AppUserChangeForm
from .models import AppUser


class AppUserAdmin(UserAdmin):
    add_form = AppUserCreationForm
    form = AppUserChangeForm
    model = AppUser
    list_display = ['profile_pic', 'gender', 'first_name', 'last_name', 'email',]


admin.site.register(AppUser, AppUserAdmin)