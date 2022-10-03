import re
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
    contact = ContactNumberSerializer(source="user_contact", many=True, required=False)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "contact")

    def update(self, instance, validated_data):
        email_data = validated_data.pop("email", instance.email)
        contact_data = validated_data.pop("contact", instance.contact_number)
        # Unless the application properly enforces that this field is
        # always set, the following could raise a `DoesNotExist`, which
        # would need to be handled.
        email = instance.email
        contact = instance.contact_number

        data = {}

        for field in self.model._meta.fields:
            if field in validated_data:
                data[field] = validated_data[field]
            else:
                data[field] = instance[field]

        user = instance.save(**data)
        Email.objects.update(user=user, email=email_data)
        ContactNumber.objects.update(user=user, contact=contact_data)

        return instance


class UserCreateSerializer(serializers.ModelSerializer):
    email = EmailSerializer(source="user_email", many=True)
    contact = ContactNumberSerializer(source="user_contact", many=True, required=False)
    password2 = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "contact",
            "password",
            "password2",
        )

    def create(self, validated_data):
        email = validated_data["user_email"][0]["email"]
        del validated_data["user_email"]
        user = User.objects.create(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        Email.objects.create(user=user, email=email)
        if "user_contact" in validated_data.keys():
            contact = validated_data.pop("user_contact")
            contact = contact[0]["contact_number"]
            ContactNumber.objects.create(user=user, contact=contact)
        return user

    def update(self, instance, validated_data):
        email_data = validated_data.pop("email", instance.email)
        contact_data = validated_data.pop("contact", instance.contact_number)
        # Unless the application properly enforces that this field is
        # always set, the following could raise a `DoesNotExist`, which
        # would need to be handled.

        email = instance.email
        contact = instance.contact_number

        data = {}

        for field in self.model._meta.fields:
            if field in validated_data:
                data[field] = validated_data[field]
            else:
                data[field] = instance[field]

        user = instance.save(**data)
        Email.objects.update(user=user, email=email_data)
        ContactNumber.objects.update(user=user, contact=contact_data)

        return instance
