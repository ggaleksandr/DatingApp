from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import AppUserManager


class AppUser(AbstractUser):
    SEX_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    username = None
    email = models.EmailField(unique=True)
    profile_pic = models.ImageField(upload_to='profile_pics/')
    gender = models.CharField(max_length=1, choices=SEX_CHOICES)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    password = models.CharField(max_length=255)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['profile_pics', 'gender', 'first_name', 'last_name']

    objects = AppUserManager()

