from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework.serializers import ModelSerializer

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
            "is_staff",
            "is_superuser",
            "last_login",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "is_staff", "is_superuser", "last_login", "created_at", "updated_at")
        extra_kwargs = {"password": {"write_only": True}}

    @transaction.atomic
    def create(self, validated_data: dict):
        employee = EmployeeModel.objects.create_user(**validated_data)
        return employee
