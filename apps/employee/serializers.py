from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from rest_framework import serializers

from apps.employee.models import UserProfile
from utils.services.email_service import EmailService

EmployeeModel = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'first_name', 'last_name', 'phone', 'avatar')


class EmployeeSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = EmployeeModel
        fields = (
            "id", "email", "password", "is_active", "is_staff", "is_superuser",
            "last_login", "created_at", "updated_at", "profile"
        )
        read_only_fields = (
            "id", "is_staff", "is_active", "is_superuser",
            "last_login", "created_at", "updated_at"
        )
        extra_kwargs = {"password": {"write_only": True}}

    @transaction.atomic
    def create(self, validated_data: dict):
        profile = validated_data.pop('profile', None)
        employee = EmployeeModel.objects.create_user(**validated_data)
        UserProfile.objects.create(**profile, user=employee)
        EmailService.register_email(employee)
        return employee


class PasswordChangeSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = EmployeeModel
        fields = ('password',)

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance
