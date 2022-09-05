from django.db import models
from django.db.models import Q
from django.contrib import auth
from django.contrib.auth import get_user_model

# from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.apps import apps
from django.core.exceptions import PermissionDenied
from django.utils.itercompat import is_iterable
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .models import User


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username and not email:
            raise ValueError("Either username or email must be present")
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        # GlobalUserModel = apps.get_model(
        #     self.model._meta.app_label, self.model._meta.object_name
        # )
        # username = GlobalUserModel.normalize_username(username)
        # username = self.normalize_username(username)
        # user = self.model(username=username, **extra_fields)
        user = User(username=username, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, email, password, **extra_fields)

    def get_by_natural_key(self, username):
        return self.get(**{self.model.USERNAME_FIELD: username})


# def with_perm(
#     self, perm, is_active=True, include_superusers=True, backend=None, obj=None
# ):
#     if backend is None:
#         backends = auth._get_backends(return_tuples=True)
#         if len(backends) == 1:
#             backend, _ = backends[0]
#         else:
#             raise ValueError(
#                 "You have multiple authentication backends configured and "
#                 "therefore must provide the `backend` argument."
#             )
#     elif not isinstance(backend, str):
#         raise TypeError(
#             "backend must be a dotted import path string (got %r)." % backend
#         )
#     else:
#         backend = auth.load_backend(backend)
#     if hasattr(backend, "with_perm"):
#         return backend.with_perm(
#             perm,
#             is_active=is_active,
#             include_superusers=include_superusers,
#             obj=obj,
#         )
#     return self.none()
