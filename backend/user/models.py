from django.apps import apps
from django.contrib import auth
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.db.models import Q

class SiteUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        if not username and not email:
            raise ValueError('Username or Email must be provided')
        email = self.normalize_email(email)

        GlobalUserModel = apps.get_model(self.model._meta.app_lable, self.model._meta.object_name)

        username = GlobalUserModel.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password, *extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("SuperUser must have is_staff=True")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("SuperUser must have is_superuser=True")

        return self._create_user(username, email, password, **extra_fields)
    
    def get_by_natural_key(self, username):
        return self.get(
            Q(username=username) | 
            Q(email=username)
        )


class SiteUser(AbstractUser):
    date_of_birth = models.DateField(blank=True, null=True)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name',]

    objects: SiteUserManager() 