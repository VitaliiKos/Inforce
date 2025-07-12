from django.contrib.auth import get_user_model
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from apps.employee.models import Employee, UserProfile
from .serializers import EmployeeSerializer, ProfileSerializer, PasswordChangeSerializer

EmployeeModel: Employee = get_user_model()


class EmployeeListView(ListAPIView):
    """List of employees"""
    serializer_class = EmployeeSerializer
    permission_classes = (IsAuthenticated, AllowAny)

    def get_queryset(self):
        queryset = EmployeeModel.objects.exclude(pk=self.request.user.pk)
        return queryset


class EmployeeDetailView(RetrieveAPIView):
    """Retrieve another employee by ID"""
    serializer_class = EmployeeSerializer
    permission_classes = (IsAuthenticated,)
    queryset = EmployeeModel.objects.all()
    lookup_field = "pk"


class UserProfileUpdateView(UpdateAPIView):
    """Update authenticated user's profile"""
    serializer_class = ProfileSerializer
    queryset = UserProfile.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user.profile


class ChangePasswordView(UpdateAPIView):
    """Change password for current user"""
    serializer_class = PasswordChangeSerializer
    permission_classes = (IsAuthenticated,)
    queryset = EmployeeModel.objects.all()

    def get_object(self):
        return self.request.user


class DeleteMyAccountView(DestroyAPIView):
    """Self-delete the authenticated user"""
    serializer_class = EmployeeSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user
