from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from utils.services.email_service import EmailService
from django.utils.timezone import now

EmployeeModel = get_user_model()


class EmployeeSerializer(ModelSerializer):
    class Meta:
        model = EmployeeModel
        fields = (
            "id",
            "email",
            "password",
            "first_name",
            "last_name",
            'is_active',
            "is_staff",
            "is_superuser",
            "last_login",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "is_staff", 'is_active', "is_superuser", "last_login", "created_at", "updated_at")
        extra_kwargs = {"password": {"write_only": True}}

    @transaction.atomic
    def create(self, validated_data: dict):
        employee = EmployeeModel.objects.create_user(**validated_data)
        EmailService.register_email(employee)
        return employee


class GoogleOAuthSerializer(serializers.Serializer):
    credential = serializers.CharField(write_only=True)
    email = serializers.EmailField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)

    def validate_credential(self, value):
        try:
            idinfo = id_token.verify_oauth2_token(value, google_requests.Request())
        except ValueError:
            raise serializers.ValidationError("Invalid Google token")

        self._google_data = {
            "email": idinfo.get("email"),
            "first_name": idinfo.get("given_name", ""),
            "last_name": idinfo.get("family_name", ""),
        }
        return value

    @transaction.atomic
    def create(self, validated_data):
        google_data = self._google_data
        employee, created = EmployeeModel.objects.get_or_create(
            email=google_data["email"],
            defaults={
                "first_name": google_data["first_name"],
                "last_name": google_data["last_name"],
                "is_active": True,
            }
        )
        if created:
            employee.set_unusable_password()
            # EmailService.register_email(employee)
            employee.save()
        employee.last_login = now()
        employee.save(update_fields=["last_login"])

        return employee
