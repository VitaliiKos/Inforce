from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils.timezone import now
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from rest_framework import serializers

from apps.employee.models import UserProfile

EmployeeModel = get_user_model()


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


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
            "phone_number": idinfo.get("phone_number", ""),
        }
        return value

    @transaction.atomic
    def create(self, validated_data):
        google_data = self._google_data
        email = google_data["email"]
        first_name = google_data["first_name"]
        last_name = google_data["last_name"]
        phone_number = google_data["phone_number"]

        employee, created = EmployeeModel.objects.get_or_create(email=email, defaults={"is_active": True})

        if created:
            UserProfile.objects.create(
                user=employee,
                first_name=first_name,
                last_name=last_name,
                phone=phone_number
            )

            employee.set_unusable_password()
            employee.save()

        employee.last_login = now()
        employee.save(update_fields=["last_login"])

        return employee
