import os

from PIL import Image
from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import AppUserManager

AVATAR_WIDTH = 300
AVATAR_HEIGHT = 300


class AppUser(AbstractUser):
    SEX_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    username = None
    email = models.EmailField(unique=True)
    profile_pic = models.ImageField(upload_to='data/profile_pics/')
    gender = models.CharField(max_length=1, choices=SEX_CHOICES)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    password = models.CharField(max_length=255)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['profile_pic', 'gender', 'first_name', 'last_name']

    objects = AppUserManager()

    # creating watermark for photo
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        profile_pic = Image.open(self.profile_pic.path).convert("RGBA")
        resized_avatar = profile_pic.resize((AVATAR_WIDTH, AVATAR_HEIGHT), Image.ANTIALIAS)
        # get current working directory independently of running OS
        cwd_name = os.getcwd()
        watermark_path = os.path.normpath(os.path.join(cwd_name, 'data/src_imgs/watermark.png'))
        watermark = Image.open(watermark_path).convert("RGBA")
        resized_avatar.paste(watermark, (0, 0), watermark)
        resized_avatar.save(self.profile_pic.path)


class Sympathy(models.Model):

    from_user = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='likes_given')
    to_user = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='likes_received')

    class Meta:
        unique_together = ('from_user', 'to_user')
