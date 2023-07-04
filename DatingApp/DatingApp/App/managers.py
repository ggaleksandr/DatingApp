from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class AppUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, profile_pic, gender, first_name, last_name, password, lat, lng, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email,
                          profile_pic=profile_pic,
                          gender=gender,
                          first_name=first_name,
                          last_name=last_name,
                          lat=lat,
                          lng=lng,
                          **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, profile_pic, gender, first_name, last_name, password, lat, lng, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, profile_pic, gender, first_name, last_name, password, lat, lng, **extra_fields)