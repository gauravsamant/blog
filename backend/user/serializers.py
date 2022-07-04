from dataclasses import field
from django.conf import settings
from django.contrib.auth import authenticate,get_user_model
from django.forms import ValidationError
from rest_framework import serializers
from rest_framework import authtoken
from .models import SiteUser

class SiteUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteUser
        fields = "__all__"

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteUser
        fields = ['email', 'password']
        extra_kwargs = {"password": {"write_only": True}}

class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField()
    class Meta:
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name', 'date_of_birth', 'contact_number']
        extra_kwargs = {
            "password": {"write_only": True},
            "password2": {"write_only": True}
        }

    def validate(self, data):
        if data['password'] != data['password2']:
            raise ValidationError("Passwords should match")