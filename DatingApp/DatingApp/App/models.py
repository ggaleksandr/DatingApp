from django.contrib.auth.models import AbstractUser
from django.db import models


class AppUser(AbstractUser):
    SEX_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    profile_pic = models.ImageField(upload_to='profile_pics/')
    gender = models.CharField(max_length=1, choices=SEX_CHOICES)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
