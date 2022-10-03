from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication


class AccessPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """

        return True

    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return True
