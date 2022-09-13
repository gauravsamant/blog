from typing_extensions import Required
from rest_framework import serializers

from .models import User, Email, ContactNumber


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = ("email",)


class ContactNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactNumber
        fields = ("contact_number",)


class UserLoginSerializer(serializers.ModelSerializer):
    email = EmailSerializer(source="user_email", many=True)
    contact = ContactNumberSerializer(source="user_contact", many=True)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "contact")
