from django.db import models
from django.db.models import Q
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend, ModelBackend
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.apps import apps
from django.core.exceptions import PermissionDenied
from django.utils.itercompat import is_iterable
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .models import Email, ContactNumber

UserModel = get_user_model()


class UserBackend(ModelBackend):
    def authenticate(
        self,
        request,
        username=None,
        email=None,
        contact_number=None,
        password=None,
        *args,
        **kwargs,
    ):

        if username is None and email is None and contact_number is None:
            return
        if password is None:
            return

        user_obj = UserModel.objects.get(
            Q(username=username)
            | Q(user_email__email=username)
            | Q(user_contact__contact_number=username)
        )

        print(user_obj)
        if user_obj is None:
            return
        if user_obj.check_password(password) and self.user_can_authenticate(user_obj):
            print(user_obj)
            return user_obj

    def get_user(self, user_id):
        try:
            user = UserModel._default_manager.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
        return user if self.user_can_authenticate(user) else None
